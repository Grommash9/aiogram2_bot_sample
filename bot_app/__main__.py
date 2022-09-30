import json
import logging
from aiogram import executor
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from bot_app import config
from bot_app.misc import dp, bot, routes, scheduler


async def on_startup(_dispatcher):
    if int(config.is_ssl):
        await bot.set_webhook(config.WEBHOOK_URL, certificate=open('/etc/nginx/ssl/nginx.crt', 'r'))
    else:
        await bot.set_webhook(config.WEBHOOK_URL)

    webhook_info = await bot.get_webhook_info()
    print(webhook_info)
    bot_data = await bot.get_me()
    print(bot_data)


    for users in config.NOTIFY_USERS:
        try:
            message_text = f"<b>@{bot_data.username} has been launched on the webhook!</b>\n\n" \
                           f"{config.WEBHOOK_HOST}/{config.ROUTE_URL}/send_message?user_id={users}&message=message%20from%20web\n\n" \
                            f"<a href='{config.WEBHOOK_HOST}/{config.ROUTE_URL}/log_errors'>Error log</a>\n\n" \
                            f"<a href='{config.WEBHOOK_HOST}/{config.ROUTE_URL}/log_output'>Output log</a>\n\n" \
                            f"{str(webhook_info)}\n\n" \
                            f"{str(bot_data)}\n\n"

            await bot.send_message(users, message_text)
        except Exception as e:
            print(e)


async def on_shutdown(_dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_bot(app: web.Application):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


if __name__ == '__main__':
    scheduler.start()
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())
    if int(config.POLLING):
        executor.start_polling(dp, skip_updates=True)
    else:
        app = get_new_configured_app(dispatcher=dp, path=f'/{config.WEBHOOK_PATH}/')
        app.add_routes(routes)
        setup_bot(app)
        web.run_app(app, **config.BOT_SERVER)

