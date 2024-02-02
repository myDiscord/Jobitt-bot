from datetime import datetime

import asyncpg
import asyncio
import logging
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from core.database.db_admins import Admins
from core.database.db_subscription import Subscription
from core.database.db_users import Users
from core.mailing.general import check_for_mailing
from core.middleware.motivator import SubMiddleware

from core.settings import settings

from core.utils.commands import set_commands
from core.utils.db_create import check_database_exists, create_database

from core.handlers.routers import user_router, admin_router
from core.utils.technologies import make_tech_list


async def start_bot(bot: Bot, users: Users, subscription: Subscription, admins: Admins) -> None:
    await set_commands(bot)
    await users.create_users_table_if_not_exists()
    await subscription.create_subscription_table_if_not_exists()
    await admins.create_admins_table_if_not_exists()
    asyncio.create_task(make_tech_list())
    await asyncio.sleep(60)
    asyncio.create_task(check_for_mailing(bot, subscription, admins))


async def stop_bot() -> None:
    pass


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.db.db_user,
        password=settings.db.db_password,
        database=settings.db.db_database,
        host=settings.db.db_host, port=settings.db.db_port,
        command_timeout=60
    )


async def start():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

    database_exists = await check_database_exists()
    if not database_exists:
        await create_database()

    bot = Bot(
        token=settings.bots.bot_token,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    pool_connect = await create_pool()
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)

    # dp.message.middleware(SubMiddleware())
    dp.callback_query.middleware(SubMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # routers
    dp.include_routers(
        user_router,
        admin_router
    )

    # database
    db_users = Users(pool_connect)
    db_subscription = Subscription(pool_connect)
    db_admins = Admins(pool_connect)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            users=db_users,
            subscription=db_subscription,
            admins=db_admins
        )
    except Exception as e:
        logging.error(f'[!!! Exception] - {e}', exc_info=True)
        with open('logs/main.log', 'a') as log_file:
            log_file.write(f'{datetime.now()} - {e}' + '\n')
    finally:
        await bot.session.close()
        await pool_connect.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
