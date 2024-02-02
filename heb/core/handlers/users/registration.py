from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from heb.core.database.db_users import Users
from heb.core.keyboards.user.menu_reply import rkb_main_menu, rkb_next, rkb_menu
from heb.core.utils.chat_cleaner import del_message, message_list
from heb.core.utils.states import UserState

router = Router()


@router.message(F.text == '✍️ Registration')
async def registration(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Enter your <b>email</b>
        """,
        parse_mode='HTML',
        reply_markup=rkb_main_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.email)


@router.message(F.text, UserState.email)
async def get_email(message: Message, bot: Bot, state: FSMContext) -> None:
    email = message.text
    await state.update_data(email=email)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Enter your <b>linked-in</b>
        """,
        parse_mode='HTML',
        reply_markup=rkb_next()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.linked_in)


@router.message(F.text, UserState.linked_in)
async def get_linked_in(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:
    linked_in = message.text
    if linked_in == '🔜 Next':
        linked_in = None

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Thank you for registering. Customize your alerts in the menu.
        """,
        reply_markup=rkb_menu()
    )
    message_list.append(msg.message_id)

    data = await state.get_data()
    email = data.get('email')
    telegram_id = message.from_user.id
    username = message.from_user.username

    await users.add_user(telegram_id, username, email, linked_in)

    await state.clear()
