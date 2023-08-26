from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from core.database.db_users import Users
from core.keyboards.admin_keyboards import rkb_admin, rkb_calendar, generate_calendar_keyboard, rkb_back
from core.utils.chat_cleaner import del_message, message_list

router = Router()


@router.message(F.text == '📊 Statistics')
async def cmd_statistic(message: Message, bot: Bot, users: Users) -> None:
    total, today_count, week, month, year = await users.get_statistics()

    c_month = datetime.now().month
    c_year = datetime.now().year

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        User stats:
        
For today: {today_count}
Weekly: {week}
Per month: {month}
For the year: {year}
Total: {total}
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
        User stats:
        
For today: {today_count}
Weekly: {week}
Per month: {month}
For the year: {year}
Total: {total}
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

    await callback.message.delete()

    msg = await callback.message.answer(
        text=f"""
        New users {c_day}.{c_month}.{c_year} - {new_users}
        """,
        reply_markup=rkb_back()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == '-')
async def empty(callback: CallbackQuery) -> None:
    await callback.answer('empty button')
