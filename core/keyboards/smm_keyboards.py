import calendar
from datetime import datetime

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def rkb_smm() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📹 Video')
    builder.button(text='💬 Text')
    builder.button(text='⚪️ Video note')
    builder.button(text='📷 Photo')

    # builder.button(text='❌📨 Cancel')
    builder.button(text='🏠 Main menu')

    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_cancel() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🚫 Cancel')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_smm_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Back')
    builder.button(text='🚫 Cancel')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_time_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📨 Send')
    builder.button(text='⌨️ Add button')
    builder.button(text='🚫 Cancel')

    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_media_time_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📨 Send')
    builder.button(text='💬 Add caption')
    builder.button(text='⌨️ Add button')
    builder.button(text='🚫 Cancel')

    builder.adjust(1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def ikb_day(month, year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    month_name = calendar.month_name[month]
    days_in_month = calendar.monthrange(year, month)[1]
    weekday = calendar.weekday(year, month, 1)
    this_monts = datetime.now().month
    empty_buttons = 0

    builder.button(text=f'{month_name} - {year}', callback_data='-')
    for days_of_week in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        builder.button(text=f'{days_of_week}', callback_data='-')

    for empty in range(weekday):
        builder.button(text=' ', callback_data='-')
        empty_buttons += 1

    for day in range(1, days_in_month + 1):
        builder.button(text=f'{day}', callback_data=f's_day_{day}_{month}_{year}')

    addition = (empty_buttons + days_in_month) % 7

    if addition != 0:
        for empty in range(7 - addition):
            builder.button(text=' ', callback_data='-')
            empty_buttons += 1
    n = (days_in_month + empty_buttons) // 7

    if month == this_monts:
        builder.button(text='⏹', callback_data='-')
    elif month == 1:
        builder.button(text='⬅️ previous', callback_data=f's_month_{12}_{year - 1}')
    else:
        builder.button(text='⬅️ previous', callback_data=f's_month_{month - 1}_{year}')

    if month == 12:
        builder.button(text='➡️ next', callback_data=f's_month_{1}_{year + 1}')
    else:
        builder.button(text='➡️ next', callback_data=f's_month_{month + 1}_{year}')
    builder.button(text='🚫 Cancel', callback_data='smm')

    builder.adjust(1, 7, * [7] * n, 2, 1)
    return builder.as_markup()


def ikb_hour() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for hour in range(24):
        builder.button(text=f'{hour}', callback_data=f's_hour_{hour}')

    builder.button(text='🚫 Cancel', callback_data='smm')

    builder.adjust(* [6] * 4, 1)
    return builder.as_markup()


def ikb_minute() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for minute in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
        builder.button(text=f'{minute}', callback_data=f's_minute_{minute}')

    builder.button(text='🚫 Cancel', callback_data='smm')

    builder.adjust(*[6] * 2, 1)
    return builder.as_markup()


def ikb_keyboard(texts, urls) -> InlineKeyboardMarkup:
    if texts:
        builder = InlineKeyboardBuilder()
        n = len(texts)
        for index in range(n):
            builder.button(text=texts[index], url=urls[index])

        builder.adjust(* [1] * n)
        return builder.as_markup()


def rkb_new_post() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📨 Send')
    builder.button(text='🚫 Cancel')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
