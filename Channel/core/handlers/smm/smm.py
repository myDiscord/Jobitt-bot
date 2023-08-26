from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_employee import Employee
from core.keyboards.smm_keyboards import ikb_smm


router = Router()


@router.message(Command(commands='smm'))
async def cmd_smm(message: Message, employee: Employee, state: FSMContext) -> None:
    await state.clear()

    result = await employee.is_user_smm(message.from_user.id)
    if result:
        await message.answer(
            text="""
            Что будем постить?
            """,
            reply_markup=ikb_smm()
        )
    else:
        await message.answer(
            text="""
            Вас нет в списке доступа
            """
        )


@router.callback_query(F.data == 'smm')
async def cmd_smm(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    await callback.message.edit_text(
        text="""
        Что будем постить?
        """,
        reply_markup=ikb_smm()
    )
