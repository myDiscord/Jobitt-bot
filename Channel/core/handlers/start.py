from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatJoinRequest, InputMediaPhoto

from core.database.db_employee import Employee
from core.database.db_users import Users
from core.database.db_welcome import Welcome

from core.keyboards.user_inline import ikb_chat, ikb_start
from core.utils.chat_cleaner import message_list

router = Router()


@router.chat_join_request()
async def request(chat_join: ChatJoinRequest, bot: Bot, users: Users) -> None:
    # add user to db
    await users.add_user(chat_join.from_user.id, chat_join.from_user.username)
    # approve chat join
    msg = await bot.send_message(
        chat_id=chat_join.from_user.id,
        text=f"""
            <b>🔥Рад приветствовать тебя!</b>
👇Жми /start для того чтоб начать!
        """,
        parse_mode='HTML'
    )
    await chat_join.approve()
    message_list.append(msg.message_id)


@router.message(Command(commands='start'))
async def cmd_start(message: Message, bot: Bot, users: Users,
                    welcome: Welcome, employee: Employee, state: FSMContext) -> None:
    await state.clear()
    user_id = message.from_user.id
    # add user to db
    await users.add_user(user_id, message.from_user.username)

    try:
        photo, caption = await welcome.get_photo()
        username = await employee.get_manager()

        await bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=caption,
            reply_markup=ikb_start(username)
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        await message.answer(
            text="""
                Тут что-то будет, когда добавят
            """
        )


@router.callback_query(F.data == 'start')
async def cmd_start(callback: CallbackQuery, bot: Bot,
                    welcome: Welcome, employee: Employee, state: FSMContext) -> None:
    await state.clear()
    user_id = callback.from_user.id

    await callback.message.delete()

    try:
        photo, caption = await welcome.get_photo()
        username = await employee.get_manager()

        await bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=caption,
            reply_markup=ikb_start(username)
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        await callback.message.answer(
            text="""
                Тут что-то будет, когда добавят
            """
        )


@router.callback_query(F.data == 'game')
async def smd_game(callback: CallbackQuery, bot: Bot, employee: Employee, welcome: Welcome) -> None:
    video, caption = await welcome.get_video()

    username = await employee.get_manager()

    await callback.message.delete()

    try:
        await bot.send_video(
            chat_id=callback.from_user.id,
            video=video,
            caption=caption,
            reply_markup=ikb_chat(username)
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        await callback.message.answer(
            text="""
                Тут что-то будет, когда добавят
            """
        )


@router.callback_query(F.data == 'review')
async def smd_review(callback: CallbackQuery, bot: Bot, employee: Employee, welcome: Welcome) -> None:
    try:
        photos, review = await welcome.get_review()
        media = list()
        for photo in photos:
            media.append(InputMediaPhoto(type='photo', media=photo))
        await bot.send_media_group(
            chat_id=callback.from_user.id,
            media=media
        )

        username = await employee.get_manager()

        await callback.message.delete()

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"""
            {review}
            """,
            reply_markup=ikb_chat(username)
        )
    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        await callback.message.answer(
            text="""
                Тут что-то будет, когда добавят
            """
        )
