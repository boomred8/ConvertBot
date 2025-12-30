from aiogram.types import (
    KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(
        KeyboardButton(text='Конвертация 📦'),
        KeyboardButton(text='Профиль 🧑🏻')
    )
    return kb.adjust(2).as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выбери дайствие'
    )


