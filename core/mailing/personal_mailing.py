import json

import asyncio

from aiogram import Bot

from core.utils.addition_data import job_types, english, experience, exp_source
from core.mailing.data_mailing import mailing


async def send_single_user_mailing(bot: Bot, telegram_id: int, subscription: dict) -> None:
    with open('sources/main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    await asyncio.sleep(30)
    for row in data:
        keywords = row['keywords'].split('/') if '/' in row['keywords'] else row['keywords'].split(' / ')

        if keywords and not any(keyword in subscription['technologies'] for keyword in keywords):
            continue

        if row['salary'] and row['salary'].isdigit() and subscription['salary_rate'] > row['salary']:
            continue

        if row['experience']:
            for key, val in exp_source.items():
                if key in row['experience']:
                    exp = exp_source[key]
                    if exp > experience[subscription['experience']]:
                        continue

        if row['experience']:
            for key, val in exp_source.items():
                if key in row['experience']:
                    exp = exp_source[key]
                    if exp > experience[subscription['experience']]:
                        continue

        if row['english_level']:
            if row['english_level'] in english.keys() and \
                    english[subscription['english_lvl']] < english[row['english_level']]:
                continue
        if job_types[row['work_type']] not in subscription['job_type']:
            continue

        await mailing(telegram_id, row, bot)
        await asyncio.sleep(60 * 5)

    with open('sources/second.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    await asyncio.sleep(60 * 5)
    for row in data:
        keywords = [spec["name"] for spec in row.get("specializations", [])]

        if keywords and not any(keyword in subscription['technologies'] for keyword in keywords):
            continue

        if row['budget2'] and row['budget2'].isdigit() and subscription['salary_rate'] >= row['budget2']:
            continue

        if row['experience']:
            for key, val in exp_source.items():
                if key in row['experience']:
                    exp = exp_source[key]
                    if exp > experience[subscription['experience']]:
                        continue

        if row['english_level']:
            if row['english_level'] in english.keys() and \
                    english[subscription['english_lvl']] < english[row['english_level']]:
                continue

        val = []
        if row['is_full_time']:
            val.append('Full time')
        if row['is_part_time']:
            val.append('Part time')
        if row['is_remote_work']:
            val.append('Remote work')
        if row['is_freelance']:
            val.append('Freelance')
        if row['is_moving']:
            val.append('Moving')
        if row['is_considering_outstaff']:
            val.append('Outstaff')

        common_values = set(val) & set(subscription['job_type'])
        if not common_values:
            continue

        await mailing(telegram_id, row, bot)
        await asyncio.sleep(60 * 5)
