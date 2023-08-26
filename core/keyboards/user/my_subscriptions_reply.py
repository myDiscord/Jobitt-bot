from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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