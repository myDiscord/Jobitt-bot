from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from core.database.db_users import Users
from core.keyboards.admin_keyboards import ikb_admin, ikb_calendar, generate_calendar_keyboard, ikb_back
from core.utils.chat_cleaner import message_list

router = Router()


@router.callback_query(F.data == 'a_statistic')
async def cmd_statistic(callback: CallbackQuery, users: Users) -> None:
    total, today_count, week, month, year = await users.get_statistics()

    c_month = datetime.now().month
    c_year = datetime.now().year

    msg = await callback.message.edit_text(
        text=f"""
        Статистика пользователей:
        
Всего: {total}
За сегодня: {today_count}
За неделю: {week}
За месяц: {month}
За год: {year}
        """,
        reply_markup=generate_calendar_keyboard(c_month, c_year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('month_'))
async def cmd_statistic(callback: CallbackQuery, users: Users) -> None:
    c_month = int(callback.data.split('_')[-2])
    c_year = int(callback.data.split('_')[-1])
    total, today_count, week, month, year = await users.get_statistics()

    msg = await callback.message.edit_text(
        text=f"""
        Статистика пользователей:

Всего: {total}
За сегодня: {today_count}
За неделю: {week}
За месяц: {month}
За год: {year}
        """,
        reply_markup=generate_calendar_keyboard(c_month, c_year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('day_'))
async def cmd_statistic(callback: CallbackQuery, users: Users) -> None:
    c_day = int(callback.data.split('_')[-3])
    c_month = int(callback.data.split('_')[-2])
    c_year = int(callback.data.split('_')[-1])

    target_datetime = datetime(c_year, c_month, c_day)
    new_users = await users.get_new_users(target_datetime)

    msg = await callback.message.edit_text(
        text=f"""
        Новых пользователей {c_day}.{c_month}.{c_year} - {new_users}
        """,
        reply_markup=ikb_back()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == '-')
async def empty(callback: CallbackQuery) -> None:
    await callback.answer('пусто')
