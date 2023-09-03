from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_post import Post
from core.keyboards.smm_keyboards import rkb_cancel, rkb_smm
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import SmmState


router = Router()


@router.message(F.text == '❌📨 Cancel')
async def cancel(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Enter the post id
        """,
        reply_markup=rkb_cancel()
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
                Post №{post_id} deleted
                """,
                reply_markup=rkb_smm()
            )
            return
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

    await message.answer(
        text=f"""
        Error, post №{post_id} not deleted
        """,
        reply_markup=rkb_smm()
    )
