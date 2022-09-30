import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot_app import db, markups
from bot_app.misc import bot, dp
from bot_app.states.user import User


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    # user_data = await db.users.create_user(message.from_user, message.get_args())
    # await state.finish()
    await bot.send_message(message.from_user.id,
                           'basic hello message',
                           reply_markup=markups.user.main.main_menu())
