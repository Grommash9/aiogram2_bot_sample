import csv
from io import StringIO, BytesIO

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import db, config
from bot_app.misc import bot, dp


def csv_creator(data_list):
    new_csvfile = StringIO()
    wr = csv.writer(new_csvfile, quoting=csv.QUOTE_ALL)
    wr.writerow(data_list[0].keys())
    wr = csv.DictWriter(new_csvfile, fieldnames=data_list[0].keys())
    for sub in data_list:
        wr.writerow(sub)
    file_to_send = BytesIO()
    file_to_send.write(new_csvfile.getvalue().encode())
    file_to_send.seek(0)
    return file_to_send


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), text='Все пользователи')
async def user_download(message: Message, state: FSMContext):
    users = await db.user.get_all()
    if len(users) == 0:
        await bot.send_message(message.from_user.id, 'Список пуст')
        return
    bot_data = await bot.get_me()
    await bot.send_document(message.from_user.id, (f'{bot_data.username}_users.csv', csv_creator(users)))
