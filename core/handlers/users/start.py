from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.user.reply import rkb_start, rkb_menu
from core.utils.chat_cleaner import del_message, message_list

router = Router()


@router.message(F.text == '📖 Main menu')
@router.message(Command(commands='start'))
async def cmd_start(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    if not await users.user_exists(message.from_user.id):
        msg = await message.answer(
            text="""
            Welcome!
Please register to get started.
            """,
            reply_markup=rkb_start
        )

    else:
        await del_message(bot, message, message_list)

        msg = await message.answer(
            text="""
            Main menu
            """,
            reply_markup=rkb_menu
        )

    message_list.append(msg.message_id)
