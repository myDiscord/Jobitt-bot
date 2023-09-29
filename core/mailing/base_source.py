from googletrans import Translator
from datetime import datetime

import asyncio

from aiogram import Bot

from core.database.db_admins import Admins
from core.database.db_base import get_vacancies
from core.database.db_subscription import Subscription

from core.keyboards.user_inline import ikb_url
from core.mailing.data_mailing import find_key_by_value
from core.utils.addition_data import experience, exp_source, english, job_types

translator = Translator()


async def mailing(telegram_id: int, data_dict: dict, bot: Bot) -> None:
    if data_dict.get('is_remote'):
        text_remote = 'Remote work'
    else:
        text_remote = 'Office'

    if data_dict.get('company'):
        company = f"<a href={data_dict['website_url']}>{data_dict['name']}</a>"
    else:
        company = f"{data_dict['company_name']}"

    if data_dict.get('salary'):
        text_salary, salary = f"\n▪️ Salary - {data_dict['salary']}", ''
        if data_dict.get('salary').isdigit():
            salary = f" #{data_dict['salary']}"
    else:
        text_salary, salary = '', ''

    if data_dict.get('work_type'):
        key_found = await find_key_by_value(job_types, data_dict.get('work_type'))
        if key_found:
            text_work_type = f"\n▪️ Work type - {key_found}"
            work_types = f" #{key_found}"
        else:
            text_work_type, work_types = '', ''
    else:
        text_work_type, work_types = '', ''

    if ' / ' in data_dict.get('keywords'):
        keywords = data_dict['keywords'].split(' / ')
        keywords = keywords.replace(' ', '')
        keyword = ' '.join(keywords)
    else:
        keyword = data_dict['keywords'].replace(' ', '')
        keyword = f" #{keyword}"

    if data_dict.get('website'):
        website = f" #{data_dict['website']}"
    else:
        website = ''

    if data_dict.get('address_eng'):
        if ',' in data_dict.get('address_eng'):
            address = data_dict['address_eng'].split(', ')
            address = ' #'.join(address)
        else:
            address = f" #{data_dict['address_eng'].replace(' ', '')}"
    else:
        address = ''

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"""
            {company}

🔘 {data_dict['name']}
{text_salary}{text_work_type}
▪️ Place of work - {text_remote}
▪️ Technologies - {data_dict['keywords']}

{data_dict['short_description']}

#JOBITT{website}{work_types}{salary}{address}{keyword}
            """,
            reply_markup=ikb_url(data_dict['url'])
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')


async def check_for_mailing_base(bot: Bot, subscription: Subscription, admins: Admins) -> None:
    while True:
        block = await admins.check_block()
        if block:
            await asyncio.sleep(60)
            continue

        last_date = await admins.get_last_date('base_source')
        data = await get_vacancies(last_date)

        for row in data:
            if row['created_at'] == last_date:
                await asyncio.sleep(60)
                break

            try:
                keywords = row.get("keywords", [])
                if ' / ' in keywords:
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
                    print(4)

                    if row['english_level']:
                        if row['english_level'] in english.keys() and \
                                english[user['english_lvl']] < english[row['english_level']]:
                            continue
                    print(3)

                    val = []
                    if row['is_remote']:
                        val.append('Remote work')
                    if row['work_type']:
                        val.append(job_types[row['work_type']])
                    print(2)

                    common_values = set(val) & set(user['job_type'])
                    if not common_values:
                        continue

                    print(1)
                    await mailing(user['telegram_id'], row, bot)

            except Exception as e:
                error_message = f'{datetime.now()} Exception {e}'
                with open('logs.txt', 'a') as log_file:
                    log_file.write(error_message + '\n')

        await admins.update_last_date('base_source', data[0]['created_at'])

        await asyncio.sleep(60)
