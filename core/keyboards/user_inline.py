from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_keyboard(texts, urls) -> InlineKeyboardMarkup:
    if texts:
        builder = InlineKeyboardBuilder()

        n = len(texts)
        for index in range(n):
            builder.button(text=texts[index], url=urls[index])

        builder.adjust(* [1] * n)
        return builder.as_markup()


def ikb_url(url) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Apply now', url=url)

    builder.adjust(1)
    return builder.as_markup()
