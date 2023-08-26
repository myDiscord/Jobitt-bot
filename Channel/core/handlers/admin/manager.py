from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_employee import Employee

from core.keyboards.admin_keyboards import ikb_back
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState

router = Router()


@router.callback_query(F.data == 'a_manager')
async def manager(callback: CallbackQuery, employee: Employee, state: FSMContext) -> None:
    await state.clear()

    manager_username = await employee.get_manager()

    msg = await callback.message.edit_text(
        text=f"""
            Менеджер @{manager_username}:
Введите <b>данные нового менеджера</b> в любом из форматов:
https://t.me/username
@username
username
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.manager_username)


@router.message(AdminState.manager_username)
async def get_username(message: Message, bot: Bot, employee: Employee, state: FSMContext) -> None:
    manager_username = message.text
    if manager_username.startswith('@'):
        manager_username = manager_username[1:]
    elif manager_username.startswith('https://t.me/'):
        manager_username = manager_username[13:]

    await employee.add_manager(manager_username)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
            Новый менеджер @{manager_username}
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    message_list.append(msg.message_id)
    await state.clear()
