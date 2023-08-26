from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):

    # employee
    smm_id = State()
    smm_username = State()

    manager_username = State()

    # welcome
    welcome = State()
    w_photo = State()

    w_button_text = State()
    w_button_url = State()

    # review
    review = State()
    r_photo = State()

    r_button_text = State()
    r_button_url = State()

    # game
    game = State()
    g_video = State()

    g_button_text = State()
    g_button_url = State()


class SmmState(StatesGroup):

    text = State()

    photo = State()
    video = State()
    media_text = State()

    circle = State()

    button_text = State()
    button_url = State()

    time = State()

    post_id = State()
