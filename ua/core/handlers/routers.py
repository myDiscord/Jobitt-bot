from aiogram import Router

from ua.core.handlers.users.start import router as start
from ua.core.handlers.users.registration import router as registration
from ua.core.handlers.users.add_subscription import router as add_subscription
from ua.core.handlers.users.my_subscription import router as my_subscription
from ua.core.handlers.users.all_subscription import router as all_subscription

from ua.core.handlers.admins.admin import router as admin
from ua.core.handlers.admins.post import router as post
from ua.core.handlers.admins.statistic import router as statistic
from ua.core.handlers.admins.download import router as download
from ua.core.handlers.admins.interests import router as interests
from ua.core.handlers.admins.technologies import router as technologies


user_router = Router()
user_router.include_routers(
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
    statistic,
    download,
    interests,
    technologies
)
