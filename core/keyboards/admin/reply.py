from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


rkb_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text=''
        ),
        KeyboardButton(
            text=''
        )
    ]
], resize_keyboard=True, one_time_keyboard=True,
    input_field_placeholder='Выбери кнопку ↓', selective=True)
