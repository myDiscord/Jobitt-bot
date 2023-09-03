import calendar
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# main
def rkb_admin() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='📨 Mailing')
    builder.button(text='📆 Statistics')

    builder.button(text='📊 Interests')
    builder.button(text='💾 Download')

    builder.button(text='🔑 Change password')
    builder.button(text='🎚 Hold')

    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_admin_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🏠 Main menu')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_back() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Back')

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


# statistic
def rkb_calendar() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    days_in_month = 31
    for day in range(1, days_in_month + 1):
        builder.button(text=str(day), callback_data=f'select_day_{day}')

    builder.button(text='🚫 Cancel', callback_data='cancel')

    builder.adjust(7, 7, 7, 7)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def generate_calendar_keyboard(month, year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    month_name = calendar.month_name[month]
    days_in_month = calendar.monthrange(year, month)[1]
    weekday = calendar.weekday(year, month, 1)
    empty_buttons = 0

    builder.button(text=f'{month_name} - {year}', callback_data='-')
    for days_of_week in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        builder.button(text=f'{days_of_week}', callback_data='-')

    for empty in range(weekday):
        builder.button(text=' ', callback_data='-')
        empty_buttons += 1

    for day in range(1, days_in_month + 1):
        builder.button(text=f'{day}', callback_data=f'day_{day}_{month}_{year}')

    addition = (empty_buttons + days_in_month) % 7

    if addition != 0:
        for empty in range(7 - addition):
            builder.button(text=' ', callback_data='-')
            empty_buttons += 1

    n = (days_in_month + empty_buttons) // 7 + 1

    if month == 1:
        builder.button(text='⬅️ previous', callback_data=f'month_{12}_{year - 1}')
    else:
        builder.button(text='⬅️ previous', callback_data=f'month_{month - 1}_{year}')

    if month == 12:
        builder.button(text='➡️ next', callback_data=f'month_{1}_{year + 1}')
    else:
        builder.button(text='➡️ next', callback_data=f'month_{month + 1}_{year}')
    builder.button(text='🏠 Main menu', callback_data='a_admin')

    builder.adjust(1, * [7] * n, 2, 2)
    return builder.as_markup()


def rkb_technologies(technologies) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🏠 Main menu')
    builder.button(text='✅ Unlock all')

    n = len(technologies)
    for button in technologies:
        builder.button(text=f'{button}')

    builder.adjust(2, * [2] * n)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
