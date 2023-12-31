from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Restart bot'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def admin_commands(bot: Bot):
    commands = [
        BotCommand(
            command='admin',
            description='Admin menu'
        ),
        BotCommand(
            command='ch4nge_pass',
            description='Change admin password'
        )
    ]

    await bot.set_my_commands(commands)
