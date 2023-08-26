from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_welcome import Welcome
from core.keyboards.admin_keyboards import ikb_back, ikb_game, ikb_admin

from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import AdminState


router = Router()


@router.callback_query(F.data == 'a_game')
async def new_game(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    msg = await callback.message.edit_text(
        text="""
            Отправь мне <b>описание</b> для игрового видео
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.game)
    message_list.append(msg.message_id)


@router.message(F.text, AdminState.game)
async def get_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    await state.update_data(text=text)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {text}

Отправь мне <b>видео</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_back()
    )
    await state.set_state(AdminState.g_video)
    message_list.append(msg.message_id)


@router.message(F.video, AdminState.g_video)
async def get_video(message: Message, bot: Bot, state: FSMContext) -> None:
    video = message.video.file_id

    data = await state.get_data()
    text = data.get('text')
    await state.update_data(video=video)

    await del_message(bot, message, message_list)

    msg = await bot.send_video(
        chat_id=message.from_user.id,
        video=video,
        caption=text,
        reply_markup=ikb_game()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'a_set_game')
async def set_game(callback: CallbackQuery, welcome: Welcome, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get('text')
    video = data.get('video')
    await welcome.update_video(video, text)

    await callback.message.delete()

    msg = await callback.message.answer(
        text="""
            Игровое видео обновлено
        """,
        reply_markup=ikb_admin()
    )
    message_list.append(msg.message_id)
