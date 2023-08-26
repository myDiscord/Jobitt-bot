from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Перезагрузить бот'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def admin_commands(bot: Bot):
    commands = [
        BotCommand(
            command='admin',
            description='Меню администратора'
        ),
        BotCommand(
            command='smm',
            description='Меню сммщика'
        ),
        BotCommand(
            command='admin',
            description='Меню Босса'
        )
    ]

    await bot.set_my_commands(commands)
