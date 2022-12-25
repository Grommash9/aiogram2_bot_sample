from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.insert(KeyboardButton('Меню'))
    m.insert(KeyboardButton('sad'))
    return m
