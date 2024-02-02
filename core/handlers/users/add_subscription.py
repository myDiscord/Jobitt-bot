import json

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_admins import Admins
from core.database.db_subscription import Subscription
from core.database.db_users import Users
from core.keyboards.user.geo_inline import ikb_countries, ikb_cities, ikb_city
from core.keyboards.user.add_subscriptions_reply import ikb_type, rkb_experience, rkb_english_lvl, ikb_technologies, \
    rkb_salary
from core.keyboards.user.menu_reply import rkb_menu, rkb_no_sub
from core.keyboards.user.my_subscriptions_reply import ikb_my_subscriptions
from core.mailing.personal import personal_mailing
from core.utils.states import UserState

router = Router()


@router.message(F.text == '⚙️️ Edit', UserState.subscriptions)
@router.message(F.text == '➕ Add subscription')
async def add_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(job_type=[])

    await message.answer(
        text="""
        Please choose <b>job type</b>
        """,
        reply_markup=ikb_type([])
    )
    await state.set_state(UserState.job_type)


@router.callback_query(F.data == 'u_back±zero', UserState.technologies)
@router.callback_query(F.data.startswith('u_work_type±'))
async def get_job_type(callback: CallbackQuery, state: FSMContext) -> None:
    job = callback.data.split('±')[-1]

    if job == 'zero':
        await state.update_data(job_type=[])
        text = 'not selected'
        job_type = []

    else:
        job_type = (await state.get_data()).get('job_type', [])
        if job in job_type:
            await callback.answer('Already on the list')
            return

        job_type.append(job)
        await state.update_data(job_type=job_type)
        text = ', '.join(job_type)

    await callback.message.edit_text(
        text=f"""
        Your <b>job types</b> - {text}
        """,
        reply_markup=ikb_type(job_type)
    )
    await state.set_state(UserState.job_type)


@router.callback_query(F.data == 'u_confirm', UserState.job_type)
async def show_tech(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(technologies=[])

    with open('core/utils/keywords.json', 'r', encoding='utf-8') as json_file:
        tech_list = json.load(json_file)

    await callback.message.edit_text(
        text=f"""
        Specify the <b>technologies</b> for which you want to receive notifications.
        """,
        reply_markup=ikb_technologies(sorted(tech_list), [], 0)
    )
    await state.set_state(UserState.technologies)


@router.callback_query(F.data.startswith('u_tech±'))
async def get_tech(callback: CallbackQuery, state: FSMContext) -> None:
    page = int(callback.data.split('±')[1])
    tech = callback.data.split('±')[-1]
    if tech.isdigit():
        technologies = (await state.get_data()).get('technologies', [])
        text = ', '.join(technologies)

        with open('core/utils/keywords.json', 'r', encoding='utf-8') as json_file:
            tech_list = json.load(json_file)

        await callback.message.edit_text(
            text=f"""
            Your <b>technologies</b> - {text}
            """,
            reply_markup=ikb_technologies(sorted(tech_list), technologies, page)
        )
        return

    technologies = (await state.get_data()).get('technologies', [])
    if tech in technologies:
        await callback.answer('Already on the list')
        return

    technologies.append(tech)

    await state.update_data(technologies=technologies)
    text = ', '.join(technologies)

    with open('core/utils/keywords.json', 'r', encoding='utf-8') as json_file:
        tech_list = json.load(json_file)

    await callback.message.edit_text(
        text=f"""
        Your <b>technologies</b> - {text}
        """,
        reply_markup=ikb_technologies(sorted(tech_list), technologies, page)
    )


@router.callback_query(F.data == 'u_confirm', UserState.technologies)
async def show_experience(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await callback.message.answer(
        text=f"""
        Your <b>work experience</b>:
        """,
        reply_markup=rkb_experience()
    )
    await state.set_state(UserState.experience)


@router.message(F.text == '🔙 Back', UserState.salary_rate)
async def show_experience(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=f"""
        Your <b>work experience</b>:
        """,
        reply_markup=rkb_experience()
    )
    await state.set_state(UserState.experience)


@router.message(F.text == '🔙 Back', UserState.experience)
async def get_job_type(message: Message, state: FSMContext) -> None:
    await state.update_data(technologies=[])

    with open('utils/keywords.json', 'r', encoding='utf-8') as json_file:
        tech_list = json.load(json_file)

    await message.answer(
        text=f"""
        Specify the <b>technologies</b> for which you want to receive notifications.
        """,
        reply_markup=ikb_technologies(sorted(tech_list), [], 0)
    )
    await state.set_state(UserState.technologies)


@router.message(F.text == '🔙 Back', UserState.english_lvl)
@router.message(F.text, UserState.experience)
async def get_experience(message: Message, state: FSMContext) -> None:
    if not message.text == '🔙 Back':
        experience = message.text
        await state.update_data(experience=experience)

    await message.answer(
        text=f"""
        <b>Salary expectations</b>:
        """,
        reply_markup=rkb_salary()
    )
    await state.set_state(UserState.salary_rate)


@router.message(F.text, UserState.salary_rate)
async def get_salary_rate(message: Message, state: FSMContext) -> None:
    salary_rate = message.text
    if not salary_rate.isdigit():
        await message.answer(
            text="""
            <b>Salary expectations</b>\n\nPlease enter a number:
            """,
            reply_markup=rkb_salary()
        )
        return

    await state.update_data(salary_rate=salary_rate)

    await message.answer(
        text=f"""
        Your <b>English level</b>:
        """,
        reply_markup=rkb_english_lvl()
    )
    await state.set_state(UserState.english_lvl)


@router.callback_query(F.data == 'u_back')
async def get_salary_rate(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await callback.message.answer(
        text="""
        Your <b>English level</b>:
        """,
        reply_markup=rkb_english_lvl()
    )
    await state.set_state(UserState.english_lvl)


@router.message(F.text, UserState.english_lvl)
async def get_english_lvl(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    print(data)
    english_lvl = message.text
    await state.update_data(english_lvl=english_lvl, countries=[], countries_name=[])

    await message.answer(
        text=f"""
        Your <b>country</b>:
        """,
        reply_markup=ikb_countries()
    )
    await state.set_state(UserState.country)


@router.message(F.text, UserState.country)
async def get_country(message: Message, state: FSMContext) -> None:
    country = message.text

    with open('geo/countries.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    iso_code = None
    for line in lines:
        fields = line.strip().split('\t')
        if fields[4] == country:
            iso_code = fields[0]
            break

    if not iso_code:
        await message.answer(
            text="""
            I don't know such a country.
            """
        )
        return

    countries = (await state.get_data()).get('countries', [])
    if country in countries:
        await message.answer('Already on the list')

    else:
        countries.append(country)
        await state.update_data(countries=countries)
        text = ', '.join(countries)

        await message.answer(
            text=f"""
            Your countries: {text}
            """
        )


@router.callback_query(F.data.startswith('country_'))
async def get_country(callback: CallbackQuery) -> None:
    current_page = int(callback.data.split('_')[-1])

    await callback.message.edit_text(
        text="""
        Your <b>country</b>:
        """,
        reply_markup=ikb_countries(current_page)
    )


@router.callback_query(F.data.startswith('u_country_'))
async def get_country(callback: CallbackQuery, state: FSMContext) -> None:
    country = callback.data.split('_')[-1]
    country_name = callback.data.split('_')[-2]

    countries = (await state.get_data()).get('countries', [])
    countries_name = (await state.get_data()).get('countries_name', [])
    if country in countries:
        await callback.answer('Already on the list')

    else:
        countries.append(country)
        countries_name.append(country_name)
        await state.update_data(countries=countries, countries_name=countries_name)

    text = ', '.join(countries)

    await callback.message.edit_text(
        text=f"""
        Countries - {text}\n\nYour <b>city</b>:
        """,
        reply_markup=ikb_cities(country)
    )
    await state.set_state(UserState.city)


@router.message(F.data == 'u_now_city')
@router.callback_query(F.data == 'u_confirm')
async def get_city(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await callback.message.answer(
        text=f"""
        Enter the name of the city
        """,
        reply_markup=ikb_city()
    )
    await state.set_state(UserState.city)


@router.message(F.text, UserState.city)
async def get_city(message: Message, state: FSMContext) -> None:
    city = message.text

    with open('geo/cities.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = None
    for line in lines:
        if city in line:
            columns = line.strip().split('\t')
            result = columns[1]

    if not result:
        await message.answer(
            text="""
            I don't know such a city.
            """,
            reply_markup=ikb_city()
        )
        return

    cities = (await state.get_data()).get('cities', [])
    if city in cities:
        await message.answer('Already on the list')

    else:
        cities.append(result)
        await state.update_data(cities=cities)
        text = ', '.join(cities)

        await message.answer(
            text=f"""
            Your cities: {text}
            """,
            reply_markup=ikb_city()
        )


@router.callback_query(F.data.startswith('u_country'))
async def get_country(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text="""
        Your <b>country</b>:
        """,
        reply_markup=ikb_countries()
    )


@router.callback_query(F.data.startswith('city_'))
async def get_city(callback: CallbackQuery, state: FSMContext) -> None:
    current_page = int(callback.data.split('_')[-1])
    data = await state.get_data()
    country = data.get('country')

    await callback.message.edit_text(
        text="""
        Your <b>city</b>:
        """,
        reply_markup=ikb_cities(country, current_page)
    )


@router.callback_query(F.data.startswith('u_city_'), UserState.city)
async def get_country(callback: CallbackQuery, state: FSMContext) -> None:
    city = callback.data.split('_')[-1]

    cities = (await state.get_data()).get('cities', [])
    countries = (await state.get_data()).get('countries', [])
    if city in cities:
        await callback.answer('Already on the list')
        return

    cities.append(city)
    await state.update_data(cities=cities)
    text = ', '.join(cities)
    text_2 = ', '.join(countries)

    await callback.message.edit_text(
        text=f"""
        Your countries - {text_2}
Your cities - {text}
        """,
        reply_markup=ikb_countries()
    )
    await state.set_state(UserState.country)


@router.callback_query(F.data == 'u_skip')
async def get_country(callback: CallbackQuery, bot: Bot, users: Users,
                      subscription: Subscription, admins: Admins, state: FSMContext) -> None:
    telegram_id = callback.from_user.id

    data = await state.get_data()
    print(data)
    job_type = data.get('job_type')
    technologies = data.get('technologies')
    experience = data.get('experience')
    salary_rate = data.get('salary_rate')
    english_lvl = data.get('english_lvl')
    country = data.get('countries')
    city = data.get('cities')

    matching_id = data.get('matching_id')

    await state.clear()

    if not matching_id:

        subscription_id = await subscription.create_subscription(telegram_id, job_type, technologies,
                                                                 experience, salary_rate, english_lvl, country, city)
        await users.add_subscriptions(telegram_id, subscription_id)

        await callback.message.delete()

        await callback.message.answer(
            text="""
            From now on, we will send you notifications based on your interests.
            """,
            reply_markup=rkb_menu()
        )

    else:
        subscription_id = None

        await subscription.update_subscription(int(matching_id), job_type, technologies,
                                               experience, salary_rate, english_lvl, country, city)

        await callback.message.delete()

        subscriptions = await users.get_subscriptions(callback.from_user.id)
        data = await subscription.get_subscription(subscriptions)

        if subscriptions:
            result = ''
            ids = {}
            counter = 1

            for sub in data:
                country, city = '', ''
                job_type = ', '.join(sub["job_type"])
                tech = ', '.join(sub["technologies"])
                if sub['country']:
                    country = ', '.join(sub["country"])
                if sub['city']:
                    city = ', '.join(sub["city"])

                result += f'{counter}: {job_type} - {tech} - {country} - {city}\n'
                ids[counter] = sub["id"]

            await callback.message.answer(
                text=f"""
                Your subscription has been updated.
{result}
                """,
                reply_markup=ikb_my_subscriptions(ids)
            )
            await state.set_state(UserState.subscriptions)

        else:
            await callback.message.answer(
                text="""
                Your subscription has been updated.
                """,
                reply_markup=rkb_no_sub()
            )

    await state.set_state(UserState.subscriptions)

    hold = await admins.get_technologies()
    block = await admins.check_block()
    if not block:
        for technology in technologies:
            if technology in hold:
                continue

            if matching_id:
                data = await subscription.get_subscription_by_id(matching_id)

            elif subscription_id:
                data = await subscription.get_subscription_by_id(subscription_id)

            await personal_mailing(bot, telegram_id, data)


@router.callback_query(F.data == '-')
async def func_pass(callback: CallbackQuery) -> None:
    await callback.answer('Not available')
