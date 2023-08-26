from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.admin_keyboards import ikb_admin, ikb_menu
from core.utils.chat_cleaner import message_list

from core.settings import settings

id_list = [
    settings.channel.owner_id,
    settings.channel.my_id
]

router = Router()


@router.message(Command(commands='admin'), F.chat.id.in_(id_list))
async def cmd_owner(message: Message, state: FSMContext) -> None:
    await state.clear()

    msg = await message.answer(
        text="""
        Меню администратора
        """,
        reply_markup=ikb_admin()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'a_admin')
async def cmd_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await callback.message.edit_text(
        text="""
        Меню администратора
        """,
        reply_markup=ikb_admin()
    )


@router.callback_query(F.data == 'a_bot')
async def cmd_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await callback.message.edit_text(
        text="""
        Обновления для меню пользователей
        """,
        reply_markup=ikb_menu()
    )
