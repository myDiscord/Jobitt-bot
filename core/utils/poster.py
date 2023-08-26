import asyncio
from aiogram import Bot
from datetime import datetime

from core.database.db_post import Post
from core.database.db_users import Users
from core.keyboards.user_inline import ikb_keyboard


async def sleeper(current_time, action_time) -> None:

    if current_time <= action_time:
        time_difference = (action_time - current_time).total_seconds()
        await asyncio.sleep(time_difference)


async def bot_poster(bot: Bot, users: Users, post: Post) -> None:
    current_time = datetime.now()

    data = await post.get_bot_row(current_time)

    if not data:
        await asyncio.sleep(1 * 60)
        await bot_poster(bot, users, post)
        return

    await sleeper(current_time, data['date_time'])

    asyncio.create_task(post_bot(bot, users, post, data))

    await bot_poster(bot, users, post)


async def post_bot(bot, users, post, data):
    telegram_ids = await users.get_users()

    for user_id in telegram_ids:
        try:
            if data['photo']:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=data['photo'],
                    caption=data['caption'],
                    reply_markup=ikb_keyboard(data['buttons_texts'], data['buttons_urls'])
                )
            elif data['video']:
                await bot.send_video(
                    chat_id=user_id,
                    video=data['video'],
                    caption=data['caption'],
                    reply_markup=ikb_keyboard(data['buttons_texts'], data['buttons_urls'])
                )
            elif data['circle']:
                await bot.send_video_note(
                    chat_id=user_id,
                    video_note=data['circle'],
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=data['text'],
                    reply_markup=ikb_keyboard(data['buttons_texts'], data['buttons_urls'])
                )
        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')

    await post.delete_row(data['id'])
