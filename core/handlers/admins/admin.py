from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.admin.inline import ikb_start
from core.settings import settings
from core.utils.chat_cleaner import del_message, del_callback, message_list

router = Router()


@router.message(Command(commands='admin'), F.chat.id == settings.bots.admin_id)
async def cmd_start(message: Message, state: FSMContext) -> None:
    msg = await message.answer(
        text="""
        Главное меню администратора
        """,
        reply_markup=ikb_start()
    )
    message_list.append(msg.message_id)