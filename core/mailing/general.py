from googletrans import Translator
from datetime import datetime

import asyncio

from aiogram import Bot

from core.database.db_admins import Admins
from core.database.db_base import new_data
from core.database.db_subscription import Subscription

from core.keyboards.user_inline import ikb_url
from core.utils.addition_data import job_types, experience, exp_source, english

translator = Translator()


async def mailing(telegram_id: int, row: dict, bot: Bot) -> None:
    if row['is_remote'] == 0:
        remote = 'Remote work'
    else:
        remote = 'Office'

    if row['company_url']:
        company = f"<a href={row['company_url']}>{row['company_name']}</a>"
    else:
        company = f"{row['company_name']}"

    if row['salary']:
        salary = f"\n▪️ Salary - {row['salary']}"
    else:
        salary = ''

    if row['work_type']:
        text_work_type = f"\n▪️ Work type - {row['work_type']:}"
        work_type = f" #{row['work_type']:}"
    else:
        text_work_type, work_type = '', ''

    if '/' in row['keywords'] or ' / ' in row['keywords']:
        keywords = f"#{row['keywords'].split('/')}" \
            if '/' in f"#{row['keywords']}" else row['keywords'].split(' / ')
        keywords = keywords.replace(' ', '')
        keyword = ' '.join(keywords)
    else:
        keyword = row['keywords'].replace(' ', '')
        keyword = f" #{keyword}"

    url = row['url']
    if url.endswith('/'):
        url += '?utm_source=JOBITT&utm_medium=BOT+&utm_campaign=JOBITT'
    else:
        url += '/?utm_source=JOBITT&utm_medium=BOT+&utm_campaign=JOBITT'

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"""
            {company}

🔘 {row['name']}
{salary}{text_work_type}
▪️ Place of work - {remote}
▪️ Technologies - {row['keywords']}

{row['short_description']}

#JOBITT{work_type}{salary}{keyword}
            """,
            reply_markup=ikb_url(url)
        )
    except Exception as e:
        with open('logs/mailing.log', 'a') as log_file:
            log_file.write(f'{datetime.now()} - {telegram_id} - Exception: {e}' + '\n')


async def check_for_mailing(bot: Bot, subscription: Subscription, admins: Admins) -> None:
    while True:
        block = await admins.check_block()
        if block:
            await asyncio.sleep(60)
            continue

        last_id = await admins.get_last_id()
        data = await new_data(last_id)
        await admins.update_last_id(data[0]["id"])

        for row in data:
            try:
                keywords = row['keywords'].split('/') if '/' in row['keywords'] else row['keywords'].split(' / ')

                all_subscriptions = await subscription.get_all_subscriptions()
                for user in all_subscriptions:

                    if keywords and not any(keyword in user['technologies'] for keyword in keywords):
                        continue
                    if row['salary'] and row['salary'].isdigit() and user['salary_rate'] >= row['salary']:
                        continue

                    if row['experience']:
                        for key, val in exp_source.items():
                            if key in row['experience']:
                                exp = exp_source[key]
                                if exp > experience[user['experience']]:
                                    continue

                    if row['english_level']:
                        if row['english_level'] in english.keys() and \
                                english[user['english_lvl']] < english[row['english_level']]:
                            continue
                    if job_types[row['work_type']] not in user['job_type']:
                        continue

                    await mailing(user['telegram_id'], row, bot)

            except Exception as e:
                with open('logs/mailing.log', 'a') as log_file:
                    log_file.write(f'{datetime.now()} Exception {e}' + '\n')

        await asyncio.sleep(60)
