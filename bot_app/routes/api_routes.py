import os
import pathlib

from bot_app import config
from aiohttp import web

from bot_app.misc import routes, bot


@routes.get(f'/{config.ROUTE_URL}/send_message')
async def get_handler(request):
    tx_data = dict(request.query)
    message_text = tx_data['message']
    user_id = tx_data['user_id']

    try:
        await bot.send_message(user_id, message_text)
    except Exception as e:
        return web.Response(status=404, body=str(e))
    return web.Response(status=200, body='ok')


@routes.get(f"/{config.ROUTE_URL}/log_errors")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_error.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))


@routes.get(f"/{config.ROUTE_URL}/log_output")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_output.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))