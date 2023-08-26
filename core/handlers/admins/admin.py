from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_admins import Admins
from core.keyboards.admin_keyboards import rkb_admin, rkb_admin_menu
from core.utils.chat_cleaner import message_list, del_message

from core.utils.states import AdminState

router = Router()


@router.message(F.text == '🏠 Main menu')
@router.message(Command(commands='addmin'))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    msg = await message.answer(
        text="""
        Enter password
        """
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.get_password)


@router.message(F.text, AdminState.get_password)
async def get_password(message: Message, bot: Bot, admins: Admins, state: FSMContext) -> None:
    password = message.text
    true_password = await admins.get_password()

    await del_message(bot, message, message_list)
    if password == true_password:
        msg = await message.answer(
            text="""
            Administrator Menu
            """,
            reply_markup=rkb_admin()
        )
        await state.clear()

    else:
        msg = await message.answer(
            text="""
            Wrong password
            """
        )
    message_list.append(msg.message_id)


@router.message(Command(commands='ch4nge_pass'))
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    msg = await message.answer(
        text="""
        Enter new password
        """,
        reply_markup=rkb_admin_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.new_password)


@router.message(F.text, AdminState.new_password)
async def get_password(message: Message, bot: Bot, admins: Admins, state: FSMContext) -> None:
    password = message.text
    true_password = await admins.set_password(password)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Password changed to {true_password}
        """,
        reply_markup=rkb_admin()
    )
    message_list.append(msg.message_id)
    await state.clear()