from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_post import Post
from core.keyboards.smm_keyboards import ikb_smm_menu
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import SmmState


router = Router()


@router.callback_query(F.data.startswith('smm_cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    msg = await callback.message.edit_text(
        text="""
            Введите id публикации
        """,
        reply_markup=ikb_smm_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.post_id)


@router.message(SmmState.post_id)
async def get_id(message: Message, bot: Bot, post: Post) -> None:
    post_id = message.text

    await del_message(bot, message, message_list)

    try:
        result = await post.delete_row(int(post_id))
        if result:
            await message.answer(
                text=f"""
                    Публикация №{post_id} удалена
                """,
                reply_markup=ikb_smm_menu()
            )
            return
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

    await message.answer(
        text=f"""
            Ошибка, публикация №{post_id} не удалена
        """,
        reply_markup=ikb_smm_menu()
    )
