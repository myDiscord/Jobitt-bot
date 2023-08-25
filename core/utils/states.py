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


class AdminState(StatesGroup):

    pass
