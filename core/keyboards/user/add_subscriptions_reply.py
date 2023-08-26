from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def rkb_type() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    types = ['Full time', 'Part time', 'Remote work', 'Freelance', 'Moving', 'Outstaff']
    n = len(types)

    for button in types:
        builder.button(text=f'{button}')
    builder.button(text='📖 Main menu')

    builder.adjust(* [2] * n, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_technologies(technologies) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(technologies)
    for button in technologies:
        builder.button(text=f'{button}')

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(* [2] * n, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_experience() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    types = ['Without experience', '0.5 years', '1 year', '1.5 years', '2 years', 'More than 5 years']
    n = len(types)

    for button in types:
        builder.button(text=f'{button}')

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(*[2] * n, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_salary() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_english_lvl() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    types = ['Without English', 'Beginner/Elementary', 'Pre-Intermediate',
             'Intermediate', 'Upper Intermediate', 'Advanced/Fluent']
    n = len(types)

    for button in types:
        builder.button(text=f'{button}')

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(*[2] * n, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
