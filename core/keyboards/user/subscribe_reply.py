from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


rkb_type = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Full time'
        ),
        KeyboardButton(
            text='Part time'
        )
    ],
    [
        KeyboardButton(
            text='Remote work'
        ),
        KeyboardButton(
            text='Freelance'
        )
    ],
    [
        KeyboardButton(
            text='Moving'
        ),
        KeyboardButton(
            text='Outstaff'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_experience = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Without experience'
        ),
        KeyboardButton(
            text='0.5 years'
        )
    ],
    [
        KeyboardButton(
            text='1 year'
        ),
        KeyboardButton(
            text='1.5 years'
        )
    ],
    [
        KeyboardButton(
            text='2 years'
        ),
        KeyboardButton(
            text='More than 5 years'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_english_lvl = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Without English'
        ),
        KeyboardButton(
            text='Beginner/Elementary'
        )
    ],
    [
        KeyboardButton(
            text='Pre-Intermediate'
        ),
        KeyboardButton(
            text='Intermediate'
        )
    ],
    [
        KeyboardButton(
            text='Upper Intermediate'
        ),
        KeyboardButton(
            text='Advanced/Fluent'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)
