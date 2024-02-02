from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_base import day_data
from core.database.db_subscription import Subscription
from core.keyboards.user.menu_reply import rkb_main_menu
from core.keyboards.user_inline import ikb_url

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

    data = await day_data(sub["job_type"], sub["technologies"], sub["experience"])
    for row in data:
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
