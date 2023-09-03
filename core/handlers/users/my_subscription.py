from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_subscription import Subscription
from core.database.db_users import Users
from core.keyboards.user.menu_reply import rkb_main_menu
from core.keyboards.user.my_subscriptions_reply import ikb_my_subscriptions, rkb_subscription
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


@router.message(F.text == '🔙 Back', UserState.subscriptions)
@router.message(F.text == '📋 My subscriptions')
async def my_subscription(message: Message, bot: Bot, users: Users,
                          subscription: Subscription, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    subscriptions = await users.get_subscriptions(message.from_user.id)
    data = await subscription.get_subscription(subscriptions)

    if subscriptions:
        msg = await message.answer(
            text="""
            Your subscriptions:
            """,
            reply_markup=ikb_my_subscriptions(data)
        )
        await state.set_state(UserState.subscriptions)

    else:
        msg = await message.answer(
            text="""
            You don't have any subscriptions yet.
            """,
            reply_markup=rkb_main_menu()
        )
    message_list.append(msg.message_id)


@router.message(F.text == '✖️ Unsubscribe')
async def unsubscribe(message: Message, bot: Bot, users: Users,
                      subscription: Subscription, state: FSMContext) -> None:
    data = await state.get_data()
    matching_id = int(data.get('matching_id'))
    telegram_id = message.from_user.id

    await users.remove_subscriptions_by_id(telegram_id, matching_id)
    await subscription.delete_subscription(matching_id)

    subscriptions = await users.get_subscriptions(message.from_user.id)
    data = await subscription.get_subscription(subscriptions)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        You have successfully unsubscribed
        """,
        reply_markup=ikb_my_subscriptions(data)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('u_tech_'), UserState.subscriptions)
async def my_subscription(callback: CallbackQuery, subscription: Subscription, state: FSMContext) -> None:
    sub_id = int(callback.data.split('_')[-1])

    data = await subscription.get_subscription_by_id(sub_id)

    await callback.message.delete()

    await state.update_data(matching_id=sub_id)

    tech = ', '.join(data["technologies"])
    msg = await callback.message.answer(
        text=f"""
        Job type: {data['job_type']}
Technology: {tech}
Experience: {data['experience']}
Salary rate: {data['salary_rate']}
English lvl: {data['english_lvl']}
        """,
        reply_markup=rkb_subscription()
    )
    message_list.append(msg.message_id)
