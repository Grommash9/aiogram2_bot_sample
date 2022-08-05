from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True)
    m.insert(KeyboardButton('Отмена'))
    return m
