from aiogram.types import (
     InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_convert_markup() -> InlineKeyboardMarkup:
    bt = InlineKeyboardBuilder()
    bt.add(
        InlineKeyboardButton(text='📄 Документ → PDF', callback_data="docx_to_pdf"),
        InlineKeyboardButton(text='📎 PDF → один файл', callback_data='merge_pdf'),
        InlineKeyboardButton(text='🗜 Сжать PDF', callback_data='squeeze'),
        InlineKeyboardButton(text='🖼 Объединить фотографии в один PDF', callback_data='combine'),
        InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_menu')
    )

    return bt.adjust(3).as_markup()

# stop to convert
def inline_stop_convert_markup() -> InlineKeyboardMarkup:
    bt = InlineKeyboardBuilder()
    bt.add(
        InlineKeyboardButton(text="stop to convert", callback_data="stop_to_convert")
    )

    return bt.adjust().as_markup()

# button for combine
def inline_combine_markup() -> InlineKeyboardMarkup:
    bt = InlineKeyboardBuilder()
    bt.add(
        InlineKeyboardButton(text='✅ Готово', callback_data="ready_to_combine"),
        InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_combine"),
        InlineKeyboardButton(text="⛔ Отмена", callback_data="cancel_combine"),
    )
    return bt.adjust(3).as_markup()

# button to merge pdf
def inline_pdf_merge_markup() -> InlineKeyboardMarkup:
    bt = InlineKeyboardBuilder()
    bt.add(
        InlineKeyboardButton(text='✅ Готово', callback_data="ready_to_merge"),
        InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_merge"),
        InlineKeyboardButton(text="⛔ Отмена", callback_data="cancel_merge"),
    )
    return bt.adjust(3).as_markup()