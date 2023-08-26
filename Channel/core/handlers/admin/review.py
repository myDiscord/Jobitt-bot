from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_welcome import Welcome
from core.keyboards.admin_keyboards import ikb_back, ikb_review, ikb_admin

from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState


router = Router()


@router.callback_query(F.data == 'a_reviews')
async def new_game(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    msg = await callback.message.edit_text(
        text="""
            Отправь мне <b>текст</b> для отзывов
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.review)
    message_list.append(msg.message_id)


@router.message(F.text, AdminState.review)
async def get_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    await state.update_data(text=text, photos=[])

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {text}

Отправь мне <b>фото</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.r_photo)
    message_list.append(msg.message_id)


@router.message(F.photo, AdminState.r_photo)
async def get_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    photo = message.photo[-1].file_id

    data = await state.get_data()
    photos = data.get('photos')
    photos.append(photo)
    await state.update_data(photos=photos)

    await del_message(bot, message, message_list)

    msg = await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption="""
            Фотография добавлена, отправь еще, чтоб добавить больше.
        """,
        reply_markup=ikb_review()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'a_set_review')
async def set_welcome(callback: CallbackQuery, welcome: Welcome, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get('text')
    photos = data.get('photos')
    await welcome.update_review(photos, text)

    await callback.message.delete()

    msg = await callback.message.answer(
        text="""
            Отзывы обновлены
        """,
        reply_markup=ikb_admin()
    )
    message_list.append(msg.message_id)
