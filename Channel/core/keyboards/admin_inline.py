import calendar
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# main
def ikb_admin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='👩‍💼 SMM', callback_data='a_smm')
    builder.button(text='👨‍💻 Manager', callback_data='a_manager')
    builder.button(text='👤 Bot', callback_data='a_bot')
    builder.button(text='📊 Статистика', callback_data='a_statistic')

    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def ikb_back() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Назад', callback_data='a_admin')

    builder.adjust(1)
    return builder.as_markup()


# employee
def ikb_ids(usernames, ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if usernames:
        n = len(usernames)
        for index in range(n):
            builder.button(text=f'{usernames[index]}',
                           callback_data=f'a_id_{usernames[index]}_{ids[index]}')

        builder.button(text='➕ Добавить', callback_data='a_add_smm')
        builder.button(text='🔙 Назад', callback_data='a_admin')

        builder.adjust(*[1] * n, 1, 1)

    else:
        builder.button(text='➕ Добавить', callback_data='a_add_smm')
        builder.button(text='🔙 Назад', callback_data='a_admin')

        builder.adjust(1, 1)
    return builder.as_markup()


def ikb_user_id() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='❌ Удалить', callback_data='o_del')
    builder.button(text='🔙 Назад', callback_data='a_admin')

    builder.adjust(1, 1)
    return builder.as_markup()


# bot
def ikb_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='👋 Приветствие', callback_data='a_welcome')
    builder.button(text='🎮 Игровое видео', callback_data='a_game')
    builder.button(text='🌠 Отзывы', callback_data='a_reviews')
    builder.button(text='🔙 Назад', callback_data='a_admin')

    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def ikb_welcome() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Обновить', callback_data='a_set_welcome')
    builder.button(text='🚫 Отмена', callback_data='a_welcome')

    builder.adjust(2)
    return builder.as_markup()


def ikb_review() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Обновить', callback_data='a_set_review')
    builder.button(text='🚫 Отмена', callback_data='a_reviews')

    builder.adjust(2)
    return builder.as_markup()


def ikb_game() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='✅ Обновить', callback_data='a_set_game')
    builder.button(text='🚫 Отмена', callback_data='a_game')

    builder.adjust(2)
    return builder.as_markup()


# statistic
def ikb_calendar() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    days_in_month = 31
    for day in range(1, days_in_month + 1):
        builder.button(text=str(day), callback_data=f'select_day_{day}')

    builder.button(text='🚫 Отмена', callback_data='cancel')

    builder.adjust(7, 7, 7, 7)
    return builder.as_markup()


def generate_calendar_keyboard(month, year) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    print(month, year)
    month_name = calendar.month_name[month]
    days_in_month = calendar.monthrange(year, month)[1]
    weekday = calendar.weekday(year, month, 1)
    empty_buttons = 0

    builder.button(text=f'{month_name} - {year}', callback_data='-')
    for days_of_week in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
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
        builder.button(text='⬅️ предыдущий', callback_data=f'month_{12}_{year -1}')
    else:
        builder.button(text='⬅️ предыдущий', callback_data=f'month_{month -1}_{year}')

    if month == 12:
        builder.button(text='➡️ следующий', callback_data=f'month_{1}_{year + 1}')
    else:
        builder.button(text='➡️ следующий', callback_data=f'month_{month + 1}_{year}')
    builder.button(text='🚪 Главное меню', callback_data='a_admin')

    builder.adjust(1, * [7] * n, 2, 2)
    return builder.as_markup()
