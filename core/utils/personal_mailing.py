import json

import asyncio

from aiogram import Bot

from core.utils.data_mailing import mailing


async def send_single_user_mailing(bot: Bot, telegram_id: int, user_keywords: list) -> None:
    with open('sources/main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    await asyncio.sleep(30)
    for row in data:
        waiting = False

        for user_keyword in user_keywords:
            keywords = None
            keyword = row['keywords']
            if '/' in keyword:
                keywords = keyword.split('/')
            elif ' / ' in keyword:
                keywords = keyword.split(' / ')

            if keywords:
                for keyword in keywords:
                    if user_keyword == keyword:
                        await mailing(telegram_id, row, bot)
                        waiting = True

            elif user_keyword == keyword:
                await mailing(telegram_id, row, bot)
                waiting = True

        if waiting:
            await asyncio.sleep(60 * 5)
