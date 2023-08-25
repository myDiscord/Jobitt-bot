from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_start() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='', callback_data='')
    builder.button(text='', callback_data='')

    builder.adjust(2)
    return builder.as_markup()
