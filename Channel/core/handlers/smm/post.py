from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.db_post import Post
from core.keyboards.smm_keyboards import ikb_smm, ikb_smm_menu, ikb_time_button, ikb_keyboard, ikb_new_post, ikb_day, \
    ikb_hour, ikb_minute
from core.utils.chat_cleaner import del_message, message_list
from core.utils.states import SmmState


router = Router()


@router.callback_query(F.data.startswith('smm_new_'))
async def new_post(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    category = callback.data.split('_')[-1]
    await state.update_data(category=category)

    if category == 'text':
        text = 'Отправь мне текст поста 💬'
        msg = await callback.message.edit_text(
            text=text,
            reply_markup=ikb_smm_menu()
        )
        await state.set_state(SmmState.text)

    elif category == 'photo':
        text = 'Отправь мне фото поста 📷'
        msg = await callback.message.edit_text(
            text=text,
            reply_markup=ikb_smm_menu()
        )
        await state.set_state(SmmState.photo)

    elif category == 'video':
        text = 'Отправь мне видео поста 📹'
        msg = await callback.message.edit_text(
            text=text,
            reply_markup=ikb_smm_menu()
        )
        await state.set_state(SmmState.video)

    else:
        text = 'Перешли мне видеосообщение поста ⚪️'
        msg = await callback.message.edit_text(
            text=text,
            reply_markup=ikb_smm_menu()
        )
        await state.set_state(SmmState.circle)
    message_list.append(msg.message_id)


@router.message(SmmState.text)
async def get_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    await state.update_data(text=text)

    await del_message(bot, message, message_list)

    text = f'{text}\n\nТекст сохранен'
    await message.answer(
        text=text,
        reply_markup=ikb_time_button()
    )


@router.message(SmmState.photo)
async def get_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    caption = message.caption
    smm_id = message.from_user.id
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo, caption=caption)

    await del_message(bot, message, message_list)

    text = '📷 Фото cохранено\nОтправь текст 💬 чтоб добавить/изменить описание'
    msg = await bot.send_photo(
        chat_id=smm_id,
        photo=photo,
        caption=caption
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=text,
        reply_markup=ikb_time_button()
    )
    message_list.append(msg.message_id)

    await state.set_state(SmmState.media_text)


@router.message(SmmState.video)
async def get_video(message: Message, bot: Bot, state: FSMContext) -> None:
    caption = message.caption
    smm_id = message.from_user.id
    video = message.video.file_id
    await state.update_data(video=video, caption=caption)

    await del_message(bot, message, message_list)

    text = '📹 Видео cохранено\nОтправь текст 💬 чтоб добавить/изменить описание'
    msg = await bot.send_video(
        chat_id=smm_id,
        video=video,
        caption=caption
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=text,
        reply_markup=ikb_time_button()
    )
    message_list.append(msg.message_id)

    await state.set_state(SmmState.media_text)


@router.message(F.text, SmmState.media_text)
async def get_media_text(message: Message, bot: Bot, state: FSMContext) -> None:
    caption = message.text
    smm_id = message.from_user.id
    await state.update_data(caption=caption)
    data = await state.get_data()
    photo = data.get('photo')
    video = data.get('video')

    await del_message(bot, message, message_list)

    if photo:
        msg = await bot.send_photo(
            chat_id=smm_id,
            photo=photo,
            caption=caption
        )

    else:
        msg = await bot.send_video(
            chat_id=smm_id,
            video=video,
            caption=caption
        )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text="""
        Установи время или добавь кнопку
        """,
        reply_markup=ikb_time_button()
    )
    message_list.append(msg.message_id)


@router.message(SmmState.circle)
async def get_circle(message: Message, bot: Bot, state: FSMContext) -> None:
    circle = message.video_note.file_id
    await state.update_data(circle=circle)
    month = datetime.now().month
    year = datetime.now().year

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
            Выбери <b>день</b>
            """,
        parse_mode='HTML',
        reply_markup=ikb_day(month, year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data == 'smm_time')
async def set_day(callback: CallbackQuery) -> None:
    month = datetime.now().month
    year = datetime.now().year

    msg = await callback.message.edit_text(
        text=f"""
        Выбери <b>день</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_day(month, year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('s_month_'))
async def set_day(callback: CallbackQuery) -> None:
    month = int(callback.data.split('_')[-2])
    year = int(callback.data.split('_')[-1])

    msg = await callback.message.edit_text(
        text=f"""
        Выбери <b>день</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_day(month, year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('s_day_'))
async def set_hour(callback: CallbackQuery, state: FSMContext) -> None:
    day = int(callback.data.split('_')[-3])
    month = int(callback.data.split('_')[-2])
    year = int(callback.data.split('_')[-1])
    await state.update_data(day=day, month=month, year=year)

    msg = await callback.message.edit_text(
        text=f"""
        Выбери <b>час</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_hour()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('s_hour_'))
async def set_minute(callback: CallbackQuery, state: FSMContext) -> None:
    hour = int(callback.data.split('_')[-1])
    await state.update_data(hour=hour)

    msg = await callback.message.edit_text(
        text=f"""
        Выбери <b>минуту</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_minute()
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('s_minute_'))
async def get_time(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    smm_id = callback.from_user.id
    minute = int(callback.data.split('_')[-1])
    await state.update_data(minute=minute)
    data = await state.get_data()
    day = int(data.get('day'))
    month = int(data.get('month'))
    year = int(data.get('year'))
    hour = int(data.get('hour'))

    await callback.message.delete()

    try:
        formatted_date = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute
        )

        if formatted_date < datetime.now():
            msg = await callback.message.answer(
                text="""
                Отправлять в прошлое незаконно!\nВыбери <b>день</b>
                """,
                parse_mode='HTML',
                reply_markup=ikb_day(month, year)
            )
            message_list.append(msg.message_id)
            return

        # await state.update_data(date=formatted_date)
        await preview(smm_id, bot, state)
        return

    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        msg = await callback.message.answer(
            text=f"""
            Выбери <b>день</b>
            """,
            parse_mode='HTML',
            reply_markup=ikb_day(month, year)
        )
        message_list.append(msg.message_id)


@router.callback_query(F.data == 'smm_button')
async def set_button(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(
        text=f"""
        Отправь мне <b>текст</b> кнопки
        """,
        parse_mode='HTML',
        reply_markup=ikb_smm_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.button_text)


@router.message(F.text, SmmState.button_text)
async def get_b_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    data = await state.get_data()
    button_text = data.get('button_text')
    if not button_text:
        button_text = []
    button_text.append(text)
    await state.update_data(button_text=button_text)

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Отправь мне <b>ссылку</b> кнопки
        """,
        parse_mode='HTML',
        reply_markup=ikb_smm_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.button_url)


@router.message(F.text, SmmState.button_url)
async def get_b_url(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    data = await state.get_data()
    button_url = data.get('button_url')
    button_text = data.get('button_text')
    if not button_url:
        button_url = []
    button_url.append(text)
    await state.update_data(button_url=button_url)
    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Кнопка(и):
        """,
        reply_markup=ikb_keyboard(button_text, button_url)
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=f"""
        Добавь кнопку или установи время
        """,
        reply_markup=ikb_time_button()
    )
    message_list.append(msg.message_id)


async def preview(smm_id: int, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    video = data.get('video')
    caption = data.get('caption')
    circle = data.get('circle')
    button_text = data.get('button_text')
    button_url = data.get('button_url')

    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour')
    minute = data.get('minute')

    if photo:
        await bot.send_photo(
            chat_id=smm_id,
            photo=photo,
            caption=caption,
            reply_markup=ikb_keyboard(button_text, button_url)
        )
    elif video:
        await bot.send_video(
            chat_id=smm_id,
            video=video,
            caption=caption,
            reply_markup=ikb_keyboard(button_text, button_url)
        )
    elif circle:
        await bot.send_video_note(
            chat_id=smm_id,
            video_note=circle
        )
    else:
        await bot.send_message(
            chat_id=smm_id,
            text=text,
            reply_markup=ikb_keyboard(button_text, button_url)
        )

    await bot.send_message(
        chat_id=smm_id,
        text=f"""
        Время отправки: {day}.{month}.{year} {hour}:{minute}
        """,
        reply_markup=ikb_new_post()
    )


@router.callback_query(F.data.endswith('_send'))
async def send(callback: CallbackQuery, post: Post, state: FSMContext) -> None:
    source = callback.data.split('_')[0]

    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    video = data.get('video')
    caption = data.get('caption')
    circle = data.get('circle')
    button_text = data.get('button_text')
    button_url = data.get('button_url')

    year = data.get('year')
    month = data.get('month')
    day = data.get('day')
    hour = data.get('hour')
    minute = data.get('minute')

    formatted_datetime = datetime(year, month, day, hour, minute)

    post_id = await post.add_row(source, text, photo, video, caption, circle,
                                 formatted_datetime, button_text, button_url)

    info = 'в '
    if source == 'channel':
        info += 'канал'
    else:
        info += 'бот'
    await callback.message.edit_text(
        text=f"""
        Пост №{post_id} {info} запланирован на {day}.{month}.{year} {hour}:{minute}
        """
    )

    await state.clear()

    await callback.message.answer(
        text=f"""
        Главное меню
        """,
        reply_markup=ikb_smm()
    )


@router.callback_query(F.data == '-')
async def empty(callback: CallbackQuery) -> None:
    await callback.answer('пусто')
