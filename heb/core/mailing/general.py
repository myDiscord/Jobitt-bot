from datetime import datetime

import asyncio

from aiogram import Bot

from heb.core.database.db_admins import Admins
from heb.core.database.db_base import new_data
from heb.core.database.db_subscription import Subscription

from heb.core.keyboards.user_inline import ikb_url


async def mailing(telegram_id: int, row: dict, bot: Bot) -> None:
    if row.get('is_remote'):
        text_remote = 'Remote work'
    else:
        text_remote = 'Office'

    if row.get('company_name'):
        company = f"<a href={row.get('company_url')}>{row.get('company_name')}</a>"
    else:
        company = f"{row.get('company_name')}"

    if row.get('salary'):
        text_salary = f"\n▪️ Salary - {row.get('salary')}"
    else:
        text_salary = ''

    if row.get('work_type'):
        text_work_type = f"\n▪️ Work type - {row.get('work_type')}"
        work_types = f"#{row.get('work_type')}"
    else:
        text_work_type, work_types = '', ''

    if ' / ' in row.get('keywords'):
        keywords = row.get('keywords').split(' / ')
        keywords = keywords.replace(' ', '')
        keyword = ' '.join(keywords)
    else:
        keyword = row.get('keywords').replace(' ', '')
        keyword = f" #{keyword}"

    if row.get('website'):
        website = f" #{row.get('website')}"
    else:
        website = ''

    url = row.get('work_url')
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
{text_salary}{text_work_type}

▪️ Place of work - {text_remote}
▪️ Technologies - {row.get('keywords')}

{row.get('short_description')}

#JOBITT{website} {work_types.replace(' ', '_')}{keyword}
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
            keywords = row.get('keywords').split('/') if '/' in row.get('keywords') else row.get('keywords').split(' / ')

            all_subscriptions = await subscription.get_all_subscriptions()
            for user in all_subscriptions:

                if keywords and not any(keyword in user.get('technologies') for keyword in keywords):
                    continue

                if row.get('work_type') and row.get('work_type') not in user.get('job_type'):
                    continue

                await mailing(user.get('telegram_id'), row, bot)

        await asyncio.sleep(60)
