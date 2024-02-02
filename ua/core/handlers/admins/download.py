import os

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from ua.core.database.db_users import Users
from ua.core.keyboards.admin_keyboards import rkb_admin_menu
from ua.core.utils.chat_cleaner import message_list, del_message, del_bot_message

router = Router()


@router.message(F.text == '💾 Download')
async def cmd_download(message: Message, bot: Bot, users: Users) -> None:
    await del_message(bot, message, message_list)

    msg = await bot.send_message(
        chat_id=message.from_user.id,
        text='⏳'
    )
    message_list.append(msg.message_id)

    directory = 'download/'
    os.makedirs(directory, exist_ok=True)
    await users.export_to_excel('users', os.path.join(directory, 'users.xlsx'))
    users_table = FSInputFile(path='download/users.xlsx')

    await del_bot_message(bot, message, message_list)

    msg = await bot.send_document(
        chat_id=message.from_user.id,
        document=users_table,
        caption=f"""
        👤 Users
        """,
        reply_markup=rkb_admin_menu()
    )
    message_list.append(msg.message_id)

    await users.export_to_excel('subscription', os.path.join(directory, 'subscription.xlsx'))
    users_table = FSInputFile(path='download/subscription.xlsx')
    msg = await bot.send_document(
        chat_id=message.from_user.id,
        document=users_table,
        caption=f"""
        📋 Subscriptions
        """
    )
    message_list.append(msg.message_id)
