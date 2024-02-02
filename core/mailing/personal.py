import asyncio
from datetime import datetime

from aiogram import Bot

from core.database.db_base import day_data
from core.keyboards.user_inline import ikb_url


async def personal_mailing(bot: Bot, telegram_id: int, sub: dict) -> None:
    await asyncio.sleep(30)
    data = await day_data(sub["job_type"], sub["technologies"], sub["experience"])
    for row in data:
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

        await asyncio.sleep(60 * 5)
