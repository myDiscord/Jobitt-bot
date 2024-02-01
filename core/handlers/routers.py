from aiogram import Router

from core.handlers.users.start import router as start
from core.handlers.users.registration import router as registration
from core.handlers.users.add_subscription import router as add_subscription
from core.handlers.users.my_subscription import router as my_subscription
from core.handlers.users.all_subscription import router as all_subscription

from core.handlers.admins.admin import router as admin
from core.handlers.admins.cancel import router as cancel
from core.handlers.admins.post import router as post
from core.handlers.admins.statistic import router as statistic
from core.handlers.admins.download import router as download
from core.handlers.admins.interests import router as interests
from core.handlers.admins.technologies import router as technologies

from core.handlers.change_status import router as channel

user_router = Router()
user_router.include_routers(
    channel,
    start,
    registration,
    add_subscription,
    my_subscription,
    all_subscription
)


admin_router = Router()
admin_router.include_routers(
    admin,
    post,
    cancel,
    statistic,
    download,
    interests,
    technologies
)
