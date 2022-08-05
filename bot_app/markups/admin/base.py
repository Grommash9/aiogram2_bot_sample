from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Рассылка'))
    m.insert(KeyboardButton('Все пользователи'))
    return m
