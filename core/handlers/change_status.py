from aiogram import Router, Bot
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.user_inline import ikb_motivator

router = Router()


@router.chat_member()
async def on_new_chat_members(message: Message, bot: Bot, users: Users):
    telegram_id = message.new_chat_member.user.id

    if message.chat.type == 'channel':
        if message.new_chat_member:
            await users.set_sub_status(telegram_id, True)
        elif message.left_chat_member:
            await users.set_sub_status(telegram_id, False)

            await bot.send_message(
                chat_id=telegram_id,
                text="""
                For the bot to work you need to be subscribed to the channel
                """,
                reply_markup=ikb_motivator()
            )

    elif message.chat.type in ['group', 'supergroup']:
        if message.new_chat_member:
            await users.set_sub_status(telegram_id, True)
        elif message.left_chat_member:
            await users.set_sub_status(telegram_id, False)

            await bot.send_message(
                chat_id=telegram_id,
                text="""
                For the bot to work you need to be subscribed to the channel
                """,
                reply_markup=ikb_motivator()
            )
