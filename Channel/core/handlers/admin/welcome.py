from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_welcome import Welcome
from core.keyboards.admin_keyboards import ikb_back, ikb_welcome, ikb_admin

from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState


router = Router()


@router.callback_query(F.data == 'a_welcome')
async def new_welcome(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    msg = await callback.message.edit_text(
        text="""
        Отправь мне <b>текст</b> приветственного сообщения
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.welcome)
    message_list.append(msg.message_id)


@router.message(F.text, AdminState.welcome)
async def get_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    await state.update_data(text=text)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {text}

Отправь мне <b>фото</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.w_photo)
    message_list.append(msg.message_id)


@router.message(F.photo, AdminState.w_photo)
async def get_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    photo = message.photo[-1].file_id

    data = await state.get_data()
    text = data.get('text')
    await state.update_data(photo=photo)

    await del_message(bot, message, message_list)

    msg = await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=text,
        reply_markup=ikb_welcome()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'a_set_welcome')
async def set_welcome(callback: CallbackQuery, welcome: Welcome, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await welcome.update_photo(photo, text)

    await callback.message.delete()

    msg = await callback.message.answer(
        text="""
        Приветственное сообщение обновлено
        """,
        reply_markup=ikb_admin()
    )
    message_list.append(msg.message_id)
