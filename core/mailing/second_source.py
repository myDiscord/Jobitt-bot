import json
from googletrans import Translator
from datetime import datetime

import asyncio

from aiogram import Bot

from core.database.db_admins import Admins
from core.database.db_subscription import Subscription

from core.keyboards.user_inline import ikb_url
from core.utils.addition_data import experience, exp_source, english, work_type

translator = Translator()


async def mailing(telegram_id: int, data_dict: dict, bot: Bot) -> None:
    if data_dict.get('is_remote_work'):
        text_remote = 'Remote work'
    else:
        text_remote = 'Office'

    if data_dict.get('company'):
        company = f"<a href={data_dict.get('company')['website_url']}>{data_dict.get('company')['name']}</a>"
    else:
        company = f"{data_dict.get('company')['name']}"

    if data_dict.get('budget'):
        text_salary, salary = f"\n▪️ Salary - {data_dict.get('budget')}", ''
        if data_dict.get('budget').isdigit():
            salary = f" #{data_dict.get('salary')}"
        if data_dict.get('budget2'):
            text_salary += f" - {data_dict.get('budget2')}",
            if data_dict.get('budget2').isdigit():
                salary += "+"
    else:
        text_salary, salary = '', ''

    extracted_data = {work_type[key]: data_dict[key] for key in work_type if data_dict[key] is True}
    if extracted_data:
        text_work_type = f"\n▪️ Work type - "
        key_found = ' '.join(extracted_data)
        text_work_type += key_found
        work_types = ' '.join(['#' + word.replace(' ', '_') for word in extracted_data])
    else:
        text_work_type, work_types = '', ''

    keywords = [spec["name"] for spec in data_dict.get("specializations", [])]
    if keywords:
        keyword_text = ' '.join(keywords)
        keyword = ' '.join(['#' + word.replace(' ', '') for word in keywords])
    else:
        keyword_text, keyword = '', ''

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"""
            {company}
            
🔘 {data_dict['name']}
{text_salary}{text_work_type}
▪️ Place of work - {text_remote}
▪️ Technologies - {keyword_text}

{data_dict['short_description']}

#JOBITT {work_types} {salary} {keyword}
            """,
            reply_markup=ikb_url(data_dict['url'])
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')


async def check_for_mailing_2(bot: Bot, subscription: Subscription, admins: Admins) -> None:
    while True:
        block = await admins.check_block()
        if block:
            await asyncio.sleep(60)
            continue

        last_date = await admins.get_last_date('second_source')
        with open('sources/second.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for row in data:
            if row['created_at'] == last_date:
                await asyncio.sleep(60)
                break

            try:
                keywords = [spec["name"] for spec in row.get("specializations", [])]

                all_subscriptions = await subscription.get_all_subscriptions()
                for user in all_subscriptions:

                    if keywords and not any(keyword in user['technologies'] for keyword in keywords):
                        continue

                    if row['budget2'] and row['budget2'].isdigit() and user['salary_rate'] >= row['budget2']:
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

                    common_values = set(val) & set(user['job_type'])
                    if not common_values:
                        continue

                    await mailing(user['telegram_id'], row, bot)

            except Exception as e:
                error_message = f'{datetime.now()} Exception {e}'
                with open('logs.txt', 'a') as log_file:
                    log_file.write(error_message + '\n')

        await admins.update_last_date('second_source', data[0]['created_at'])

        await asyncio.sleep(60)
