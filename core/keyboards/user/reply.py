from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


rkb_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='✍️ Registration'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_main_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📖 Main menu'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_next = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='🔜 Next'
        ),
        KeyboardButton(
            text='📖 Main menu'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='📋 My subscriptions'
        )
    ],
    [
        KeyboardButton(
            text='➕ Add subscription'
        )
    ],
    # [
    #     KeyboardButton(
    #         text='👤 My account'
    #     )
    # ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)


rkb_account = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Unsubscribe'
        )
    ],
    [
        KeyboardButton(
            text='Extend'
        )
    ],
    [
        KeyboardButton(
            text='Invoices'
        )
    ]
], resize_keyboard=True, one_time_keyboard=False, selective=True)
