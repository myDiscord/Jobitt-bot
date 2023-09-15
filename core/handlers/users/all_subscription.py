import asyncio
import json
from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.types import Message
from core.keyboards.user.menu_reply import rkb_main_menu
from core.mailing.data_mailing import mailing

router = Router()


@router.message(F.text == '👁‍🗨 All vacancies')
async def all_subscription(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id

    await message.answer(
        text="""
        All vacancies for the month:
        """,
        reply_markup=rkb_main_menu()
    )

    with open('sources/main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for row in data:
        try:
            await mailing(user_id, row, bot)
            await asyncio.sleep(0.01)

        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')

    with open('sources/second.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for row in data:
        try:
            await mailing(user_id, row, bot)
            await asyncio.sleep(0.01)

        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')