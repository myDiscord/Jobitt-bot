from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_start() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='✍️ Registration')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📖 Main menu')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_next() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔜 Next')
    builder.button(text='📖 Main menu')

    builder.adjust(1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📋 My subscriptions')
    builder.button(text='➕ Add subscription')
    # builder.button(text='👤 My account')

    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_account() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Unsubscribe')
    builder.button(text='Extend')
    builder.button(text='Invoices')
    builder.button(text='📖 Main menu')

    builder.adjust(1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
