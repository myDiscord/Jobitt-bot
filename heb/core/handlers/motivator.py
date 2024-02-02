from aiogram import Bot

from ua.core.keyboards.user_inline import ikb_motivator


async def need_sub(user_id: int, bot: Bot) -> None:
    await bot.send_message(
        chat_id=user_id,
        text="""
        For the bot to work you need to be subscribed to the channel
        """,
        reply_markup=ikb_motivator()
    )
