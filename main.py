import asyncpg
import asyncio
import logging
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from core.database.db_admins import Admins
from core.database.db_post import Post
from core.database.db_subscription import Subscription
from core.database.db_users import Users

from core.settings import settings

from core.utils.commands import set_commands
from core.mailing.data_mailing import check_for_mailing
from core.utils.db_create import check_database_exists, create_database
from core.utils.download_data import update_json
from core.utils.poster import bot_poster
from core.utils.technologies import create_tech_list

from core.handlers.routers import user_router, admin_router


async def start_bot(bot: Bot, users: Users, subscription: Subscription, post: Post, admins: Admins) -> None:
    await set_commands(bot)
    await users.create_users_table_if_not_exists()
    await subscription.create_subscription_table_if_not_exists()
    await admins.create_admins_table_if_not_exists()
    await post.create_post_table_if_not_exists()
    asyncio.create_task(update_json())
    asyncio.create_task(create_tech_list())
    asyncio.create_task(check_for_mailing(bot, subscription, admins))
    asyncio.create_task(bot_poster(bot, users, post))
    # await bot.send_message(settings.bots.admin_id, text='Bot works')


async def stop_bot(bot: Bot) -> None:
    # await bot.send_message(settings.bots.admin_id, text='Bot doesn't works')
    pass


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.db.db_user, password=settings.db.db_password, database=settings.db.db_database,
        host=settings.db.db_host, port=settings.db.db_port, command_timeout=60
    )


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                        handlers=[logging.FileHandler("bot_logs.txt"), logging.StreamHandler()]
                        )

    database_exists = await check_database_exists()
    if not database_exists:
        await create_database()

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    pool_connect = await create_pool()
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        user_router,
        admin_router
    )

    db_users = Users(pool_connect)
    db_subscription = Subscription(pool_connect)
    db_post = Post(pool_connect)
    db_admins = Admins(pool_connect)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            users=db_users,
            subscription=db_subscription,
            post=db_post,
            admins=db_admins
        )
    except Exception as ex:
        logging.error(f'[!!! Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
