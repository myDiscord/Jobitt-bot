from aiogram import Bot, Router
from aiogram.types import Message


router = Router()
message_list = list()


async def del_message(bot: Bot, message: Message, msg_list: list) -> None:
    for message_id in msg_list:
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message_id)
        except:
            pass
    await message.delete()
    msg_list.clear()
