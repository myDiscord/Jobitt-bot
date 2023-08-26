from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_subscription import Subscription
from core.database.db_users import Users
from core.keyboards.user.geo_inline import ikb_countries, ikb_cities
from core.keyboards.user.add_subscriptions_reply import rkb_type, rkb_experience, rkb_english_lvl, rkb_technologies, \
    rkb_salary
from core.keyboards.user.menu_reply import rkb_menu
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import UserState
from core.utils.technologies import tech

router = Router()


@router.message(F.text == '⚙️️ Edit', UserState.subscriptions)
@router.message(F.text == '🔙 Back', UserState.technologies)
@router.message(F.text == '➕ Add subscription')
async def add_subscription(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    msg = await message.answer(
        text="""
        Please choose <b>job type</b>
        """,
        parse_mode='HTML',
        reply_markup=rkb_type()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.job_type)


@router.message(F.text == '🔙 Back', UserState.experience)
@router.message(F.text, UserState.job_type)
async def get_job_type(message: Message, bot: Bot, state: FSMContext) -> None:
    if not message.text == '🔙 Back':
        job_type = message.text
        await state.update_data(job_type=job_type)
    else:
        data = await state.get_data()
        job_type = data.get('job_type')

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {job_type}\nSpecify the <b>technologies</b> for which you want to receive notifications.
        """,
        parse_mode='HTML',
        reply_markup=rkb_technologies(tech)
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.technologies)


@router.message(F.text == '🔙 Back', UserState.salary_rate)
@router.message(F.text, UserState.technologies)
async def get_technologies(message: Message, bot: Bot, state: FSMContext) -> None:
    if not message.text == '🔙 Back':
        technologies = message.text
        await state.update_data(technologies=technologies)
    else:
        data = await state.get_data()
        technologies = data.get('technologies')

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {technologies}\nYour <b>work experience</b>:
        """,
        parse_mode='HTML',
        reply_markup=rkb_experience()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.experience)


@router.message(F.text == '🔙 Back', UserState.english_lvl)
@router.message(F.text, UserState.experience)
async def get_experience(message: Message, bot: Bot, state: FSMContext) -> None:
    if not message.text == '🔙 Back':
        experience = message.text
        await state.update_data(experience=experience)
    else:
        data = await state.get_data()
        experience = data.get('experience')

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {experience}\n<b>Salary expectations</b>:
        """,
        parse_mode='HTML',
        reply_markup=rkb_salary()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.salary_rate)


@router.message(F.text, UserState.salary_rate)
async def get_salary_rate(message: Message, bot: Bot, state: FSMContext) -> None:
    salary_rate = message.text
    await state.update_data(salary_rate=salary_rate)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {salary_rate}\nYour <b>English level</b>:
        """,
        parse_mode='HTML',
        reply_markup=rkb_english_lvl()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.english_lvl)


@router.callback_query(F.data == 'u_back')
async def get_salary_rate(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    msg = await callback.message.answer(
        text="""
        Your <b>English level</b>:
        """,
        parse_mode='HTML',
        reply_markup=rkb_english_lvl()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.english_lvl)


@router.message(F.text, UserState.english_lvl)
async def get_english_lvl(message: Message, bot: Bot, state: FSMContext) -> None:
    english_lvl = message.text
    await state.update_data(english_lvl=english_lvl)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        {english_lvl}\nYour <b>country</b>:
        """,
        parse_mode='HTML',
        reply_markup=ikb_countries()
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.country)


@router.callback_query(F.data.startswith('country_'))
async def get_country(callback: CallbackQuery) -> None:
    current_page = int(callback.data.split('_')[-1])

    msg = await callback.message.edit_text(
        text="""
        Your <b>country</b>:
        """,
        parse_mode='HTML',
        reply_markup=ikb_countries(current_page)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('u_country'))
async def get_country(callback: CallbackQuery) -> None:
    msg = await callback.message.edit_text(
        text="""
        Your <b>country</b>:
        """,
        parse_mode='HTML',
        reply_markup=ikb_countries()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('u_country_'), UserState.country)
async def get_country(callback: CallbackQuery, state: FSMContext) -> None:
    country = callback.data.split('_')[-1]
    country_name = callback.data.split('_')[-2]
    await state.update_data(country=country, country_name=country_name)

    msg = await callback.message.edit_text(
        text=f"""
        {country} - {country_name}\nYour <b>city</b>:
        """,
        parse_mode='HTML',
        reply_markup=ikb_cities(country)
    )
    message_list.append(msg.message_id)
    await state.set_state(UserState.city)


@router.callback_query(F.data.startswith('city_'))
async def get_city(callback: CallbackQuery, state: FSMContext) -> None:
    current_page = int(callback.data.split('_')[-1])
    data = await state.get_data()
    country = data.get('country')

    msg = await callback.message.edit_text(
        text="""
        Your <b>city</b>:
        """,
        parse_mode='HTML',
        reply_markup=ikb_cities(country, current_page)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'u_skip')
@router.callback_query(F.data.startswith('u_city_'), UserState.city)
async def get_country(callback: CallbackQuery, users: Users, subscription: Subscription, state: FSMContext) -> None:
    if callback.data != 'next':
        city = callback.data.split('_')[-1]
        await state.update_data(city=city)
    telegram_id = callback.from_user.id

    data = await state.get_data()
    job_type = data.get('job_type')
    technologies = data.get('technologies')
    experience = data.get('experience')
    salary_rate = data.get('salary_rate')
    english_lvl = data.get('english_lvl')
    country = data.get('country')
    city = data.get('city')

    matching_id = data.get('matching_id')
    if not matching_id:

        subscription_id = await subscription.create_subscription(telegram_id, job_type, technologies,
                                                                 experience, salary_rate, english_lvl, country, city)
        await users.add_subscriptions(telegram_id, subscription_id)

        await callback.message.delete()

        msg = await callback.message.answer(
            text="""
            From now on, we will send you notifications based on your interests.
            """,
            reply_markup=rkb_menu()
        )

    else:
        await subscription.update_subscription(int(matching_id), job_type, technologies,
                                               experience, salary_rate, english_lvl, country, city)

        await callback.message.delete()

        msg = await callback.message.answer(
            text="""
            Your subscription has been updated.
            """,
            reply_markup=rkb_menu()
        )

    message_list.append(msg.message_id)

    await state.clear()