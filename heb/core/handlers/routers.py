from aiogram import Router

from heb.core.handlers.users.start import router as start
from heb.core.handlers.users.registration import router as registration
from heb.core.handlers.users.add_subscription import router as add_subscription
from heb.core.handlers.users.my_subscription import router as my_subscription
from heb.core.handlers.users.all_subscription import router as all_subscription

from heb.core.handlers.admins.admin import router as admin
from heb.core.handlers.admins.post import router as post
from heb.core.handlers.admins.statistic import router as statistic
from heb.core.handlers.admins.download import router as download
from heb.core.handlers.admins.interests import router as interests
from heb.core.handlers.admins.technologies import router as technologies


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
