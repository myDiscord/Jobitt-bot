import math

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from heb.core.utils.geo import load_countries, load_cities


def ikb_countries(current_page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    countries = load_countries()

    buttons_per_page = 10
    start_index = current_page * buttons_per_page
    end_index = min(start_index + buttons_per_page, len(countries))
    buttons_to_show = list(countries.items())[start_index:end_index]
    n = min(end_index - start_index, buttons_per_page)

    for country_code, country_name in buttons_to_show:
        builder.button(text=f"{country_code}: {country_name}", callback_data=f"u_country_{country_name}_{country_code}")

    if current_page == 0:
        b_back = '⏹'
        callback_back = '-'
    else:
        b_back = '⬅️ Back'
        callback_back = f'country_{current_page - 1}'
    builder.button(text=b_back, callback_data=callback_back)

    builder.button(text=f'{current_page + 1} / {math.ceil(len(countries) / buttons_per_page)}',
                   callback_data='-')

    if end_index < len(countries):
        b_next = 'Next ➡️'
        callback_next = f'country_{current_page + 1}'
    else:
        b_next = '⏹'
        callback_next = '-'
    builder.button(text=b_next, callback_data=callback_next)

    builder.button(text='🔙 Back', callback_data='u_back')
    builder.button(text='⏭ Skip', callback_data='u_skip')
    builder.button(text='⏩ Cities', callback_data='u_now_city')
    builder.button(text='✅ Confirm', callback_data='u_confirm')

    builder.adjust(*[1] * n, 3, 2, 2)
    return builder.as_markup()


def ikb_cities(country_code, current_page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    cities = load_cities()
    city_list = cities[country_code]

    buttons_per_page = 10
    start_index = current_page * buttons_per_page
    end_index = min(start_index + buttons_per_page, len(city_list))
    buttons_to_show = city_list[start_index:end_index]
    n = min(end_index - start_index, buttons_per_page)

    for city in buttons_to_show:
        builder.button(text=f"{city}", callback_data=f"u_city_{city}")

    if current_page == 0:
        b_back = '⏹'
        callback_back = '-'
    else:
        b_back = '⬅️ Back'
        callback_back = f'city_{current_page - 1}'
    builder.button(text=b_back, callback_data=callback_back)

    builder.button(text=f'{current_page + 1} / {math.ceil(len(city_list) / buttons_per_page)}',
                   callback_data='-')

    if end_index < len(city_list):
        b_next = 'Next ➡️'
        callback_next = f'city_{current_page + 1}'
    else:
        b_next = '⏹'
        callback_next = '-'
    builder.button(text=b_next, callback_data=callback_next)

    builder.button(text='🔙 Back', callback_data='u_country')
    builder.button(text='⏭ Skip', callback_data='u_skip')
    builder.button(text='✅ Confirm', callback_data='u_confirm')

    builder.adjust(*[1] * n, 3, 2, 1)
    return builder.as_markup()


def ikb_city() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='🔙 Back', callback_data='u_country')
    builder.button(text='⏭ Skip', callback_data='u_skip')
    builder.button(text='✅ Confirm', callback_data='u_skip')

    builder.adjust(2, 1)
    return builder.as_markup()
