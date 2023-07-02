from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_app.misc import _

def admin_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton(_('Все')))
    return m
