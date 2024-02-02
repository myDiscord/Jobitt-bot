from typing import List, Callable, Union, Dict, Any, Awaitable

from aiogram import Bot, BaseMiddleware
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import CallbackQuery, Message
from cachetools import TTLCache

from core.handlers.motivator import need_sub
from core.settings import settings


class SubMiddleware(BaseMiddleware):
    caches = TTLCache(maxsize=10_000, ttl=5 * 60)

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data["bot"]
        user_id = event.from_user.id

        if user_id in self.caches:
            return await handler(event, data)

        channel_ids = await check_sub(user_id, bot)

        if channel_ids:
            await need_sub(user_id, bot)
            return

        self.caches[event.from_user.id] = True

        return await handler(event, data)


async def check_sub(user_id: int, bot: Bot) -> List[int]:
    channels = [settings.channels.channel_id]
    channel_ids = []

    for channel in channels:
        try:
            user = await bot.get_chat_member(
                chat_id=channel, user_id=user_id
            )
        except (TelegramBadRequest, TelegramForbiddenError):
            continue

        if user.status == ChatMemberStatus.LEFT:
            channel_ids.append(channel)

    return channel_ids
