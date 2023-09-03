from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def ikb_my_subscriptions(data) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    n = len(data)
    for button in data:
        text = ''
        if button['country']:
            text += f" - {button['country']}"
        if button['city']:
            text += f" - {button['city']}"
        tech = ', '.join(button["technologies"])
        builder.button(text=f'{button["job_type"]} - {tech}{text}',
                       callback_data=f'u_tech_{button["id"]}')

    builder.button(text='📖 Main menu', callback_data='start')

    builder.adjust(*[1] * n, 1)
    return builder.as_markup()


def rkb_my_subscriptions(data) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    n = len(data)

    for button in data:
        text = ''
        if button['country']:
            text += f" - {button['country']}"
        if button['city']:
            text += f" - {button['city']}"
        builder.button(text=f'{button["job_type"]} - {button["technologies"]}{text}')
    builder.button(text='📖 Main menu')

    builder.adjust(* [1] * n, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def rkb_subscription() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='⚙️️ Edit')
    builder.button(text='✖️ Unsubscribe')
    builder.button(text='🔙 Back')
    builder.button(text='📖 Main menu')

    builder.adjust(1, 1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)