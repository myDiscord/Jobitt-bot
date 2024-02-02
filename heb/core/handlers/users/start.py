from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from heb.core.database.db_users import Users
from heb.core.keyboards.user.menu_reply import rkb_start, rkb_menu
from heb.core.utils.chat_cleaner import message_list

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
            reply_markup=rkb_start()
        )

    else:
        # await del_message(bot, message, message_list)

        msg = await message.answer(
            text="""
            Main menu
            """,
            reply_markup=rkb_menu()
        )

    message_list.append(msg.message_id)


@router.callback_query(F.data == 'start')
async def cmd_start(callback: CallbackQuery, bot: Bot, users: Users, state: FSMContext) -> None:
    await state.clear()

    await callback.message.delete()

    msg = await callback.message.answer(
        text="""
        Main menu
        """,
        reply_markup=rkb_menu()
    )

    message_list.append(msg.message_id)
