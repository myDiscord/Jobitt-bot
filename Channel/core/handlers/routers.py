from aiogram import Router

from core.handlers.smm.smm import router as smm_router
# from core.handlers.smm.bot_post import router as bot_post
from core.handlers.smm.post import router as channel_post
from core.handlers.smm.cancel import router as cancel

from core.handlers.admin.admin import router as admin_router
from core.handlers.admin.smm import router as add_smm
from core.handlers.admin.manager import router as add_manager
from core.handlers.admin.welcome import router as welcome
from core.handlers.admin.game import router as game
from core.handlers.admin.review import router as review
from core.handlers.admin.statistic import router as statistic

smm = Router()

smm.include_routers(
    smm_router,
    # bot_post,
    channel_post,
    cancel
)

admin = Router()

admin.include_routers(
    admin_router,
    add_smm,
    add_manager,
    welcome,
    game,
    review,
    statistic
)
