from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def ikb_type(job_type: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    types = ['Full time', 'Part time', 'Remote work', 'Hybrid Remote', 'Freelance', 'Moving', 'Outstaff']

    for work_type in types:
        text = '✅' if work_type in job_type else ''
        builder.button(text=f'{work_type}{text}', callback_data=f'u_work_type±{work_type}')

    builder.button(text='✅ Confirm', callback_data='u_confirm')
    builder.button(text='📖 Main menu', callback_data='start')

    builder.adjust(2, 2, 2, 1, 2)
    return builder.as_markup()


def ikb_technologies(tech_list: list, technologies: list, page: int, buttons: int = 50) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    start_index = page * buttons
    end_index = min(start_index + buttons, len(tech_list))
    n = min(end_index - start_index, buttons)

    for technology in tech_list[start_index:end_index]:
        text = '✅' if technology in technologies else ''
        builder.button(text=f'{technology}{text}', callback_data=f'u_tech±{page}±{technology}')

    if page == 0:
        builder.button(text='⏹', callback_data='-')
    else:
        builder.button(text='⬅️ Previous', callback_data=f'u_tech±{page - 1}')

    if end_index < len(tech_list):
        builder.button(text='➡️ Next', callback_data=f'u_tech±{page + 1}')
    else:
        builder.button(text='⏹', callback_data='-')

    builder.button(text='🔙 Back', callback_data='u_back±zero')
    builder.button(text='📖 Main menu', callback_data='start')
    builder.button(text='✅ Confirm', callback_data='u_confirm')

    builder.adjust(* [2] * n, 1, 2, 2)
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
