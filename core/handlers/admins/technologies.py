import asyncio
from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_admins import Admins
from core.keyboards.admin_keyboards import rkb_technologies, rkb_back, rkb_admin_menu
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState
from core.utils.tech import tech_list

router = Router()


async def remove_technology(user_id: int, technology: str, hours: int, bot: Bot, admins: Admins) -> None:
    await asyncio.sleep(60 * 60 * hours)
    await admins.remove_technologies(technology)

    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"""
            {technology} removed from hold list
            """
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')


@router.message(F.text == '✅ Unlock all')
async def settings(message: Message, bot: Bot, admins: Admins) -> None:
    await admins.remove_all_technologies()

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        All technologies <b>removed</b> from hold list
        """,
        parse_mode='HTML',
        reply_markup=rkb_admin_menu()
    )
    message_list.append(msg.message_id)


@router.message(F.text == '🔙 Back', AdminState.technology_time)
@router.message(F.text == '🎚 Publications settings')
async def settings(message: Message, bot: Bot, admins: Admins, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    hold = await admins.get_technologies()
    text = ''.join([f'\n{tech}' for tech in hold])

    msg = await message.answer(
        text=f"""
            Hold list:{text}
            """
    )
    message_list.append(msg.message_id)
    msg = await message.answer(
        text=f"""
        Select the <b>technology</b> for which the publication will be suspended
        """,
        parse_mode='HTML',
        reply_markup=rkb_technologies(sorted(tech_list))
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.technology)


@router.message(F.text, AdminState.technology)
async def get_technology(message: Message, bot: Bot, admins: Admins, state: FSMContext) -> None:
    technology = message.text
    await state.update_data(technology=technology)
    await admins.add_technologies(technology)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Specify the <b>number of hours</b> for which the publication will be paused
        """,
        parse_mode='HTML',
        reply_markup=rkb_back()
    )
    message_list.append(msg.message_id)

    await state.set_state(AdminState.technology_time)


@router.message(F.text, AdminState.technology_time)
async def get_technology(message: Message, bot: Bot, admins: Admins, state: FSMContext) -> None:
    hours = message.text
    if not hours.isdigit():
        msg = await message.answer(
            text=f"""
            Please enter <b>number of hours</b> in numbers
            """,
            parse_mode='HTML',
            reply_markup=rkb_back()
        )
        message_list.append(msg.message_id)
        return

    data = await state.get_data()
    technology = data.get('technology')
    user_id = message.from_user.id

    asyncio.create_task(remove_technology(user_id, technology, int(hours), bot, admins))

    await del_message(bot, message, message_list)

    hold = await admins.get_technologies()
    text = ''.join([f'\n{tech}' for tech in hold])

    msg = await message.answer(
        text=f"""
                Hold list:{text}
                """
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=f"""
        Select the <b>technology</b> for which the publication will be suspended
        """,
        parse_mode='HTML',
        reply_markup=rkb_technologies(sorted(tech_list))
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.technology)
