import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_smm() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='📹 Видео', callback_data='smm_new_video')
    builder.button(text='💬 Текст', callback_data='smm_new_text')
    builder.button(text='⚪️ Видеосообщение', callback_data='smm_new_circle')
    builder.button(text='📷 Фото', callback_data='smm_new_photo')

    builder.button(text='❌ Отмена поста', callback_data='smm_cancel')

    builder.adjust(2, 2, 1)
    return builder.as_markup()


def ikb_smm_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Назад', callback_data='smm')

    builder.adjust(1)
    return builder.as_markup()


def ikb_time_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='⏱ Выбрать время', callback_data='smm_time')
    builder.button(text='⌨️ Добавить кнопку', callback_data='smm_button')
    builder.button(text='🚫 Отмена', callback_data='smm')

    builder.adjust(1, 1, 1)
    return builder.as_markup()


def ikb_day(month, year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    month_name = calendar.month_name[month]
    days_in_month = calendar.monthrange(year, month)[1]
    weekday = calendar.weekday(year, month, 1)
    this_monts = datetime.now().month
    empty_buttons = 0

    builder.button(text=f'{month_name} - {year}', callback_data='-')
    for days_of_week in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
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
        builder.button(text='⬅️ предыдущий', callback_data=f's_month_{12}_{year -1}')
    else:
        builder.button(text='⬅️ предыдущий', callback_data=f's_month_{month -1}_{year}')

    if month == 12:
        builder.button(text='➡️ следующий', callback_data=f's_month_{1}_{year + 1}')
    else:
        builder.button(text='➡️ следующий', callback_data=f's_month_{month + 1}_{year}')
    builder.button(text='🚫 Отмена', callback_data='smm')

    builder.adjust(1, 7, * [7] * n, 2, 1)
    return builder.as_markup()


def ikb_hour() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for hour in range(24):
        builder.button(text=f'{hour}', callback_data=f's_hour_{hour}')

    builder.button(text='🚫 Отмена', callback_data='smm')

    builder.adjust(* [6] * 4, 1)
    return builder.as_markup()


def ikb_minute() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for minute in range(60):
        builder.button(text=f'{minute}', callback_data=f's_minute_{minute}')

    builder.button(text='🚫 Отмена', callback_data='smm')

    builder.adjust(*[6] * 10, 1)
    return builder.as_markup()


def ikb_keyboard(texts, urls) -> InlineKeyboardMarkup:
    if texts:
        builder = InlineKeyboardBuilder()
        n = len(texts)
        for index in range(n):
            builder.button(text=texts[index], url=urls[index])

        builder.adjust(* [1] * n)
        return builder.as_markup()


def ikb_new_post() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='📺 Канал', callback_data='channel_send')
    builder.button(text='🤖 Бот', callback_data='bot_send')
    builder.button(text='🚫 Отмена', callback_data='smm')

    builder.adjust(1, 1, 1)
    return builder.as_markup()
