from datetime import datetime

from aiogram import Bot, Router
from aiogram.types import Message, CallbackQuery

router = Router()
message_list = list()


async def del_message(bot: Bot, message: Message, msg_list: list) -> None:
    for message_id in msg_list:
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message_id)
        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')
    await message.delete()
    msg_list.clear()


async def del_callback(bot: Bot, callback: CallbackQuery, msg_list: list) -> None:
    for message_id in msg_list:
        try:
            await bot.delete_message(
                chat_id=callback.from_user.id,
                message_id=message_id)
        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')
    msg_list.clear()


async def del_bot_message(bot: Bot, message: Message, msg_list: list) -> None:
    for message_id in msg_list:
        try:
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message_id)
        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')
    msg_list.clear()
