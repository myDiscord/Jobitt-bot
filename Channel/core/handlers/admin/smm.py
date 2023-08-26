from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_employee import Employee

from core.keyboards.admin_keyboards import ikb_admin, ikb_back, ikb_ids, ikb_user_id
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState

router = Router()


@router.callback_query(F.data == 'a_smm')
async def smm(callback: CallbackQuery, employee: Employee, state: FSMContext) -> None:
    await state.clear()

    usernames, ids = await employee.get_smm()

    await callback.message.edit_text(
        text=f"""
            SMM:
        """,
        reply_markup=ikb_ids(usernames, ids)
    )


@router.callback_query(F.data == 'a_add_smm')
async def add(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        text=f"""
            Введите <b>id</b> SMM:
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.smm_id)


@router.message(AdminState.smm_id)
async def get_id(message: Message, bot: Bot, state: FSMContext) -> None:
    smm_id = int(message.text)
    await state.update_data(smm_id=smm_id)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
            Введите <b>имя/никнейм</b> SMM:
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    message_list.append(msg.message_id)
    await state.set_state(AdminState.smm_username)


@router.message(AdminState.smm_username)
async def get_username(message: Message, bot: Bot, employee: Employee, state: FSMContext) -> None:
    smm_username = message.text
    data = await state.get_data()
    smm_id = int(data.get('smm_id'))

    await employee.add_smm(smm_id, smm_username)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
            Добавлен SMM\n{smm_username} - {smm_id}
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    message_list.append(msg.message_id)
    await state.clear()


@router.callback_query(F.data.startswith('a_id_'))
async def some_smm(callback: CallbackQuery, state: FSMContext) -> None:
    smm_id = int(callback.data.split('_')[-1])
    smm_username = callback.data.split('_')[-2]
    await state.update_data(smm_id=smm_id, smm_username=smm_username)

    await callback.message.edit_text(
        text=f"""
            {smm_username} - {smm_id}
        """,
        reply_markup=ikb_user_id()
    )


@router.callback_query(F.data == 'o_del')
async def del_smm(callback: CallbackQuery, employee: Employee, state: FSMContext) -> None:
    data = await state.get_data()
    smm_id = int(data.get('smm_id'))
    smm_username = data.get('smm_username')

    await employee.delete_smm(smm_id)

    await callback.message.edit_text(
        text=f"""
        {smm_username} - {smm_id} удален
        """,
        reply_markup=ikb_admin()
    )
    await state.clear()
