import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import config
from bot_app import db, markups
from bot_app.misc import bot, dp
from bot_app.states.admin import Admin


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Рассылка')
async def mass_send_to_all(message: Message, state: FSMContext):
    await state.set_state(Admin.MassSend.to_all_message)
    await bot.send_message(message.from_user.id,
                           'Пришлите сообщение для рассылки',
                           reply_markup=markups.base.cancel_menu())


@dp.message_handler(text='Отмена', state=Admin.MassSend.to_all_message)
async def cancel_mass_send(message: Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'Рассылка отменена',
                           reply_markup=markups.admin.base.admin_menu())


@dp.message_handler(content_types=aiogram.types.ContentType.ANY, state=Admin.MassSend.to_all_message)
async def get_mass_send_message(message: Message, state: FSMContext):
    errors_list = []
    good, bad = 0, 0
    await state.finish()
    user_list = await db.user.get_all()

    await bot.send_message(message.from_user.id,
                           f"Рассылка запущена для {len(user_list)} пользователей",
                           reply_markup=markups.admin.base.admin_menu())
    for users in user_list:
        try:
            await bot.copy_message(users['user_id'],
                                   message_id=message.message_id,
                                   from_chat_id=message.chat.id)
            good += 1
        except Exception as e:
            errors_list.append(str(e))
            bad += 1
    await bot.send_message(message.from_user.id,
                           f"Рассылка завершена!\n"
                           f"Доставлено: {good}\n"
                           f"Не доставлено: {bad}\n\n"
                           f"Список ошибок: {set(errors_list)}")
