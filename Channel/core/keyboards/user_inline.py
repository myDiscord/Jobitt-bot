from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_start(username) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='💬 Напиши мне', url=f't.me/{username}')
    builder.button(text='🎮 Показать программу и игру', callback_data='game')
    builder.button(text='🚀 Отзывы', callback_data='review')

    builder.adjust(1, 1, 1)
    return builder.as_markup()


def ikb_chat(username) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='💬 Напиши мне', url=f't.me/{username}')
    builder.button(text='🔙 Назад', callback_data='start')

    builder.adjust(1, 1)
    return builder.as_markup()


def ikb_keyboard(texts, urls) -> InlineKeyboardMarkup:
    if texts:
        builder = InlineKeyboardBuilder()
        n = len(texts)
        for index in range(n):
            builder.button(text=texts[index], url=urls[index])

        builder.adjust(* [1] * n)
        return builder.as_markup()
