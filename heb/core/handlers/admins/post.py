from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from heb.core.database.db_users import Users
from heb.core.keyboards.smm_keyboards import rkb_smm, rkb_smm_menu, rkb_time_button, ikb_keyboard, rkb_new_post, ikb_day, \
    ikb_hour, ikb_minute, rkb_cancel, rkb_media_time_button
from heb.core.utils.chat_cleaner import del_message, message_list, del_callback
from heb.core.utils.states import SmmState


router = Router()


@router.message(F.text == '🔙 Back', SmmState.post_id)
@router.message(F.text == '🔙 Back', SmmState.text)
@router.message(F.text == '🔙 Back', SmmState.photo)
@router.message(F.text == '🔙 Back', SmmState.video)
@router.message(F.text == '🔙 Back', SmmState.circle)
@router.message(F.text == '🚫 Cancel')
@router.message(F.text == '📨 Mailing')
async def cmd_smm(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    await state.clear()

    msg = await message.answer(
        text="""
        Select message type:
        """,
        reply_markup=rkb_smm()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.post)


@router.callback_query(F.data == 'smm')
async def cmd_smm(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await state.clear()

    await callback.message.answer(
        text="""
        Select message type:
        """,
        reply_markup=rkb_smm()
    )
    await state.set_state(SmmState.post)


@router.message(F.text, SmmState.post)
async def new_post(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()

    category = message.text
    await state.update_data(category=category, button_text=[], button_url=[])

    await del_message(bot, message, message_list)

    if category == '💬 Text':
        text = 'Send me the text of the post 💬'
        msg = await message.answer(
            text=text,
            reply_markup=rkb_smm_menu()
        )
        await state.set_state(SmmState.text)

    elif category == '📷 Photo':
        text = 'Send me a post photo 📷'
        msg = await message.answer(
            text=text,
            reply_markup=rkb_smm_menu()
        )
        await state.set_state(SmmState.photo)

    elif category == '📹 Video':
        text = 'Send me a post video 📹'
        msg = await message.answer(
            text=text,
            reply_markup=rkb_smm_menu()
        )
        await state.set_state(SmmState.video)

    else:
        text = 'Forward me the video message of the post ⚪️'
        msg = await message.answer(
            text=text,
            reply_markup=rkb_smm_menu()
        )
        await state.set_state(SmmState.circle)
    message_list.append(msg.message_id)


@router.message(SmmState.text)
async def get_text(message: Message, bot: Bot, state: FSMContext) -> None:
    text = message.text
    await state.update_data(text=text)

    await del_message(bot, message, message_list)

    text = f'{text}\n\nText saved'
    msg = await message.answer(
        text=text,
        reply_markup=rkb_time_button()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.time)


@router.message(SmmState.photo)
async def get_photo(message: Message, bot: Bot, state: FSMContext) -> None:
    caption = message.caption
    smm_id = message.from_user.id
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo, caption=caption)

    await del_message(bot, message, message_list)

    text = '📷 Photo saved\nSend text 💬 to add/change description'
    msg = await bot.send_photo(
        chat_id=smm_id,
        photo=photo,
        caption=caption
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=text,
        reply_markup=rkb_media_time_button()
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

    text = '📹 Video saved\nSubmit text 💬 to add/change description'
    msg = await bot.send_video(
        chat_id=smm_id,
        video=video,
        caption=caption
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=text,
        reply_markup=rkb_media_time_button()
    )
    message_list.append(msg.message_id)

    await state.set_state(SmmState.media_text)


@router.message(F.text == '💬 Add caption', SmmState.media_text)
async def get_media_text(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)
    text = 'Send me caption of the post 💬'
    msg = await message.answer(
        text=text,
        reply_markup=rkb_smm_menu()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.get_media_text)


@router.message(F.text, SmmState.get_media_text)
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
        Set the time or add a button
        """,
        reply_markup=rkb_time_button()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.time)


@router.message(SmmState.circle)
async def get_circle(message: Message, bot: Bot, state: FSMContext) -> None:
    circle = message.video_note.file_id
    await state.update_data(circle=circle)
    month = datetime.now().month
    year = datetime.now().year

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Choose <b>day</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_day(month, year)
    )
    message_list.append(msg.message_id)


@router.message(F.text == '⏱ Select time', SmmState.time)
@router.message(F.text == '⏱ Select time', SmmState.button_url)
@router.message(F.text == '⏱ Select time', SmmState.circle)
@router.message(F.text == '⏱ Select time', SmmState.media_text)
async def set_day(message: Message, bot: Bot) -> None:
    month = datetime.now().month
    year = datetime.now().year

    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Choose <b>day</b>
        """,
        parse_mode='HTML',
        reply_markup=ikb_day(month, year)
    )
    message_list.append(msg.message_id)


@router.callback_query(F.data.startswith('s_month_'))
async def set_day(callback: CallbackQuery, bot: Bot) -> None:
    month = int(callback.data.split('_')[-2])
    year = int(callback.data.split('_')[-1])

    await del_callback(bot, callback, message_list)
    msg = await callback.message.edit_text(
        text=f"""
        Choose <b>day</b>
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
        Choose <b>hour</b>
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
        Choose <b>minute</b>
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
                Sending to the past is illegal!\nChoose <b>day</b>
                """,
                parse_mode='HTML',
                reply_markup=ikb_day(month, year)
            )
            message_list.append(msg.message_id)
            return

        await preview(smm_id, bot, state)
        return

    except Exception as e:
        error_message = f'{datetime.now()} Exception {e}'
        with open('logs.txt', 'a') as log_file:
            log_file.write(error_message + '\n')

        msg = await callback.message.answer(
            text=f"""
            Choose <b>day</b>
            """,
            parse_mode='HTML',
            reply_markup=ikb_day(month, year)
        )
        message_list.append(msg.message_id)


@router.message(F.text == '🔙 Back', SmmState.button_text)
@router.message(F.text == '⌨️ Add button', SmmState.time)
@router.message(F.text == '⌨️ Add button', SmmState.media_text)
async def set_button(message: Message, bot: Bot, state: FSMContext) -> None:
    await del_message(bot, message, message_list)

    msg = await message.answer(
        text=f"""
        Send me <b>text</b> for button
        """,
        parse_mode='HTML',
        reply_markup=rkb_cancel()
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
        Send me <b>link</b> for button\nIn format https://.... (https://t.me/none)
        """,
        parse_mode='HTML',
        reply_markup=rkb_smm_menu()
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
        Button(s):
        """,
        reply_markup=ikb_keyboard(button_text, button_url)
    )
    message_list.append(msg.message_id)

    msg = await message.answer(
        text=f"""
        Add a button or set a time
        """,
        reply_markup=rkb_time_button()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.time)


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

    msg = await bot.send_message(
        chat_id=smm_id,
        text=f"""
        Send time: {day}.{month}.{year} {hour}:{minute}
        """,
        reply_markup=rkb_new_post()
    )
    message_list.append(msg.message_id)

    await state.set_state(SmmState.send)


@router.message(F.text == '📨 Send', SmmState.time)
@router.message(F.text == '📨 Send', SmmState.button_url)
@router.message(F.text == '📨 Send', SmmState.circle)
@router.message(F.text == '📨 Send', SmmState.media_text)
async def send(message: Message, bot: Bot, users: Users, state: FSMContext) -> None:

    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    video = data.get('video')
    caption = data.get('caption')
    circle = data.get('circle')
    button_text = data.get('button_text')
    button_url = data.get('button_url')

    await del_message(bot, message, message_list)

    await state.clear()

    msg = await message.answer(
        text=f"""
        Select message type:
        """,
        reply_markup=rkb_smm()
    )
    message_list.append(msg.message_id)
    await state.set_state(SmmState.post)

    telegram_ids = await users.get_users()

    for user_id in telegram_ids:
        try:
            if photo:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=ikb_keyboard(button_text, button_url)
                )
            elif video:
                await bot.send_video(
                    chat_id=user_id,
                    video=video,
                    caption=caption,
                    reply_markup=ikb_keyboard(button_text, button_url)
                )
            elif circle:
                await bot.send_video_note(
                    chat_id=user_id,
                    video_note=circle
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=text,
                    reply_markup=ikb_keyboard(button_text, button_url)
                )
        except Exception as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')


@router.callback_query(F.data == '-')
async def empty(callback: CallbackQuery) -> None:
    await callback.answer('empty')
