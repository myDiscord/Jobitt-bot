from aiogram import Router

from core.handlers.users.start import router as start
from core.handlers.users.registration import router as registration
from core.handlers.users.add_subscription import router as add_subscription
from core.handlers.users.my_subscription import router as my_subscription


user_router = Router()
user_router.include_routers(
    start,
    registration,
    add_subscription,
    my_subscription
)
