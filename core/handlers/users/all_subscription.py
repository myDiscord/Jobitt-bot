from datetime import datetime
from dateutil.relativedelta import relativedelta

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_base import get_vacancies_by_interest
from core.database.db_subscription import Subscription
from core.keyboards.user.menu_reply import rkb_main_menu
from core.keyboards.user_inline import ikb_url
from core.mailing.data_mailing import find_key_by_value
from core.utils.addition_data import job_types, english, experience, exp_source

router = Router()


@router.message(F.text == '👁‍🗨 All vacancies')
async def all_subscription(message: Message, bot: Bot, subscription: Subscription, state: FSMContext) -> None:
    telegram_id = message.from_user.id

    await message.answer(
        text="""
        All vacancies for the month:
        """,
        reply_markup=rkb_main_menu()
    )

    data = await state.get_data()
    matching_id = int(data.get('matching_id'))
    sub = await subscription.get_subscription_by_id(matching_id)

    one_month_ago = datetime.now() - relativedelta(months=1)
    data = await get_vacancies_by_interest(one_month_ago)

    for row in data:
        keywords = row['keywords'].split(' / ')

        if keywords and not any(keyword in sub['technologies'] for keyword in keywords):
            continue

        if row['salary'] and row['salary'].isdigit() and sub['salary_rate'] >= row['salary']:
            continue

        if row['experience']:
            for key, val in exp_source.items():
                if key in row['experience']:
                    exp = exp_source[key]
                    if exp > experience[sub['experience']]:
                        continue

        if row['english_level']:
            if row['english_level'] in english.keys() and \
                    english[sub['english_lvl']] < english[row['english_level']]:
                continue

        val = []
        if row['is_remote']:
            val.append('Remote work')
        if row['work_type']:
            val.append(job_types[row['work_type']])

        common_values = set(val) & set(sub['job_type'])
        if not common_values:
            continue

        await mailing(telegram_id, row, bot)


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
