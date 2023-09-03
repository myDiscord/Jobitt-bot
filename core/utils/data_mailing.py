import json
from googletrans import Translator
from datetime import datetime

import asyncio

from aiogram import Bot

from core.database.db_admins import Admins
from core.database.db_subscription import Subscription

from core.keyboards.user_inline import ikb_url


translator = Translator()


async def mailing(telegram_id: int, data_dict: dict, bot: Bot) -> None:
    if data_dict.get('is_remote_work'):
        remote = ' #RemoteWork'
        text_remote = 'Remote work'
    else:
        remote = ''
        text_remote = 'Office'

    if data_dict.get('company')['website_url']:
        company = f"<a href={data_dict.get('company')['website_url']}>{data_dict.get('company')['name']} looks for:</a>"
    else:
        company = f"{data_dict.get('company')['name']} looks for:"

    if data_dict.get('salary'):
        salary = f"\n▪️ Salary - {data_dict.get('salary')}"
    else:
        salary = ''

    is_type = {
        'неполная занятость': 'Part time',
        'полная занятость': 'Full time'
    }

    if data_dict.get('work_type') in is_type:
        work_type = f"\n▪️ Work type - {is_type[data_dict.get('work_type')]}"
    else:
        work_type = ''

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"""
            {company}

🔘 {data_dict['name']}
{salary}{work_type}
▪️ Place of work - {text_remote}
▪️ Technologies - {data_dict['keywords']}

{data_dict['short_description']}

#vacancy{remote} #jobitt
            """,
            reply_markup=ikb_url(data_dict.get('url'))
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')


async def check_for_mailing(bot: Bot, subscription: Subscription, admins: Admins) -> None:
    last_id = await admins.get_last_processed_data()
    with open('sources/main.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    await admins.update_last_processed_data(data[0]['created_at'])

    hold = await admins.get_technologies()

    is_type = {
        'неполная занятость': 'Part time',
        'полная занятость': 'Full time',
        'повний робочий день': 'Full time'
    }

    for row in data:
        if row['created_at'] == last_id:
            await asyncio.sleep(60 * 1)
            await check_for_mailing(bot, subscription, admins)

        keywords = None
        keyword = row['keywords']
        if '/' in keyword:
            keywords = keyword.split('/')
        elif ' / ' in keyword:
            keywords = keyword.split(' / ')
        if keywords:
            for keyword in keywords:
                if keyword in hold:
                    continue
        else:
            if keyword in hold:
                continue

        all_subscriptions = await subscription.get_all_subscriptions()
        for user in all_subscriptions:
            if keywords:
                for keyword in keywords:
                    if keyword not in user['technologies']:
                        continue
                if user['city']:
                    if user['city'] != row['address_eng']:
                        continue
                if row['salary'] and row['salary'].isdigit():
                    if user['salary_rate'] < row['salary']:
                        continue
                if row['work_type']:
                    if user['job_type'] != is_type[row['work_type'].lower()]:
                        continue

            else:
                if keyword not in user['technologies']:
                    continue
                if user['city']:
                    if user['city'] != row['address_eng']:
                        continue
                if row['salary'] and row['salary'].isdigit():
                    if user['salary_rate'] < row['salary']:
                        continue
                if row['work_type']:
                    if user['job_type'] != is_type[row['work_type']]:
                        continue

                await mailing(user['telegram_id'], row, bot)

    await asyncio.sleep(60 * 1)
    await check_for_mailing(bot, subscription, admins)
