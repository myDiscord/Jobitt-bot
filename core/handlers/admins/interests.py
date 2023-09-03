from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_subscription import Subscription
from core.keyboards.admin_keyboards import rkb_admin_menu
from core.utils.chat_cleaner import message_list, del_message

router = Router()


@router.message(F.text == '📊 Interests')
async def cmd_start(message: Message, subscription: Subscription, bot: Bot, state: FSMContext) -> None:
    await state.clear()

    await del_message(bot, message, message_list)

    categories = ['job_type', 'technologies', 'experience', 'english_lvl', 'country', 'city']
    msg = await message.answer(
        text="""
        Interests:
        """,
        reply_markup=rkb_admin_menu()
    )
    message_list.append(msg.message_id)

    for category in categories:
        stats = await subscription.get_statistic_by_category(category)
        text = f"{category.capitalize()} total: {stats['total']}"
        for subcategory, count in stats['details'].items():
            subcategory = subcategory.strip('{}"')
            text += f"\n- {subcategory} - {count}"

        msg = await message.answer(
            text=text
        )
        message_list.append(msg.message_id)
