from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):

    email = State()
    linked_in = State()

    job_type = State()
    technologies = State()
    experience = State()
    salary_rate = State()
    english_lvl = State()

    country = State()
    city = State()

    subscriptions = State()


class AdminState(StatesGroup):

    get_password = State()
    new_password = State()

    admin_menu = State()

    statistic = State()

    technology = State()
    technology_time = State()


class SmmState(StatesGroup):

    post = State()

    text = State()

    photo = State()
    video = State()
    media_text = State()
    get_media_text = State()

    circle = State()

    button_text = State()
    button_url = State()

    time = State()
    send = State()

    post_id = State()
