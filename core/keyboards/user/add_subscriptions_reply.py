from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def ikb_type() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    types = ['Full time', 'Part time', 'Remote work', 'Hybrid Remote', 'Freelance', 'Moving', 'Outstaff']

    for work_type in types:
        builder.button(text=f'{work_type}', callback_data=f'u_work_type±{work_type}')

    builder.button(text='✅ Confirm', callback_data='u_confirm')
    builder.button(text='📖 Main menu', callback_data='start')

    builder.adjust(2, 2, 2, 1, 2)
    return builder.as_markup()


def ikb_technologies(technologies) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(technologies)
    for technology in technologies:
        builder.button(text=f'{technology}', callback_data=f'u_tech±{technology}')

    builder.button(text='✅ Confirm', callback_data='u_confirm')
    builder.button(text='🔙 Back', callback_data='u_back±zero')
    builder.button(text='📖 Main menu', callback_data='start')

    builder.adjust(* [2] * n, 1, 2)
    return builder.as_markup()


def rkb_experience() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    types = ['Without experience', '0.5 years', '1 year', '1.5 years', '2 years', 'More than 5 years']
    n = len(types)

    for button in types:
        builder.button(text=f'{button}')

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(*[2] * n, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_salary() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def rkb_english_lvl() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    types = ['Without English', 'Beginner/Elementary', 'Pre-Intermediate',
             'Intermediate', 'Upper-Intermediate', 'Advanced/Fluent']
    n = len(types)

    for button in types:
        builder.button(text=f'{button}')

    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(*[2] * n, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
