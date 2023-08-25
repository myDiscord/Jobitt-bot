from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.db_users import Users
from core.keyboards.user.subscribe_reply import rkb_type, rkb_experience, rkb_english_lvl
from core.keyboards.user.reply import rkb_main_menu, rkb_menu, rkb_next
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState

router = Router()


@router.message(F.text == '➕ Add subscription')
async def add_subscription(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Please choose <b>job type</b>
        """,
        parse_mode='HTML',
        reply_markup=rkb_type
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.job_type)


@router.message(F.text, UserState.job_type)
async def get_job_type(message: Message, bot: Bot, state: FSMContext) -> None:
    job_type = message.text
    await state.update_data(job_type=job_type)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Specify the <b>technologies</b> for which you want to receive notifications.
        """,
        parse_mode='HTML',
        reply_markup=rkb_main_menu
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.technologies)


@router.message(F.text, UserState.technologies)
async def get_technologies(message: Message, bot: Bot, state: FSMContext) -> None:
    technologies = message.text
    await state.update_data(technologies=technologies)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Your work experience:
        """,
        parse_mode='HTML',
        reply_markup=rkb_experience
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.experience)


@router.message(F.text, UserState.experience)
async def get_experience(message: Message, bot: Bot, state: FSMContext) -> None:
    experience = message.text
    await state.update_data(experience=experience)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Salary expectations:
        """,
        parse_mode='HTML',
        reply_markup=rkb_main_menu
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.salary_rate)


@router.message(F.text, UserState.salary_rate)
async def get_salary_rate(message: Message, bot: Bot, state: FSMContext) -> None:
    salary_rate = message.text
    await state.update_data(salary_rate=salary_rate)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Your English level:
        """,
        parse_mode='HTML',
        reply_markup=rkb_english_lvl
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.english_lvl)


@router.message(F.text, UserState.english_lvl)
async def get_english_lvl(message: Message, bot: Bot, state: FSMContext) -> None:
    english_lvl = message.text
    await state.update_data(english_lvl=english_lvl)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Your country:
        """,
        parse_mode='HTML',
        reply_markup=rkb_next
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.country)


@router.message(F.text, UserState.country)
async def get_country(message: Message, bot: Bot, state: FSMContext) -> None:
    country = message.text
    if country != '🔜 Next':
        await state.update_data(country=country)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Your city:
        """,
        parse_mode='HTML',
        reply_markup=rkb_next
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.city)


@router.message(F.text, UserState.city)
async def get_city(message: Message, bot: Bot, state: FSMContext) -> None:
    city = message.text
    if city != '🔜 Next':
        await state.update_data(city=city)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Thank you for registering. From now on, we will send you notifications based on your interests.
        """,
        parse_mode='HTML',
        reply_markup=rkb_menu
    )
    message_list.append(msg.message_id)
    await state.clear()
