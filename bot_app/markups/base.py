from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


def language_menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.insert(InlineKeyboardButton(text='🇺🇦 Українська', callback_data='set-lang_uk'))
    m.insert(InlineKeyboardButton(text='🇺🇸 English', callback_data='set-lang_en'))
    return m
