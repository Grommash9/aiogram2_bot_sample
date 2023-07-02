import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from bot_app.misc import bot, dp, _, _l
from bot_app import markups, config
from bot_app.misc import bot, dp


@dp.message_handler(aiogram.filters.IDFilter(chat_id=config.ADMINS_ID), commands=['admin'], state='*')
async def process_start(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           _('Admin menu here'),
                           reply_markup=markups.admin.base.admin_menu())
