
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_app.misc import _


def main_menu(locale):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton(_('👛 Wallets', locale=locale)))
    m.insert(KeyboardButton(_('👨 Change Language', locale=locale)))
    return m
