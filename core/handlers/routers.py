from aiogram import Router

from core.handlers.users.start import router as start
from core.handlers.users.registration import router as registration
from core.handlers.users.add_subscribe import router as subscribe


user_router = Router()
user_router.include_routers(
    start,
    registration,
    subscribe
)
