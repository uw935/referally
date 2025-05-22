import json

from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram import (
    F,
    Router
)
from aiogram.types import (
    Message,
    CallbackQuery
)

from ...log import UserLog
from ...database import User
from ...captcha import Captcha
from ...texts import TextFormatter
from .menu import send_channel_link
from ...keyboard import create_markup
from ...states import (
    CaptchaState,
    ReffedUserState
)


router = Router()
router.message.filter(CaptchaState.CAPTCHA)
router.callback_query.filter(CaptchaState.CAPTCHA)


async def send_captcha_message(
    message: Message,
    state: FSMContext,
    lang_code: str | None = None
) -> None:
    """
    Sending message with captcha in it

    :param message: Telegram message
    :param state: User's state
    :param lang_code: User's language code. Needed if the message was sent by
    the bot.
    """

    state_data = await state.get_data()

    if state_data.get("captcha_id") is None:
        await start_captcha_process(message, state, lang_code)
        return

    lang_code = lang_code or message.from_user.language_code
    keyboard = json.loads(state_data["captcha_keyboard"])["inline_keyboard"]

    await message.answer(
        TextFormatter(
            "captcha:text",
            lang_code,
            element=TextFormatter(
                f"captcha:{state_data['captcha_text']}",
                lang_code
            ).text
        ).text,
        reply_markup=create_markup(
            *[
                [
                    button for button in keyboard[index]
                ]
                for index in range(0, len(keyboard))
            ]
        )
    )


async def start_captcha_process(
    message: Message,
    state: FSMContext,
    lang_code: str | None = None
) -> None:
    """
    Starting captcha point

    :param message: Telegram message
    :param state: User's state
    :param lang_code: User's language code, if message was sent by the bot.
    Helpful for callbacks
    """

    await state.set_state(CaptchaState.CAPTCHA)

    captcha = Captcha("CAPTCHA_PROCEED").generate()
    logger.info(f"Generated captcha with ID: {captcha.id}")

    await state.set_data({
        "captcha_keyboard": captcha.keyboard.model_dump_json(),
        "captcha_text": captcha.text,
        "captcha_id": captcha.id,
        "captcha_attempt": 0
    })

    await send_captcha_message(message, state, lang_code)


@router.callback_query(F.data[:15] == "CAPTCHA_PROCEED")
async def captcha_proceed_handler(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    """
    Captcha proceed handler

    :param callback: Telegram Callback
    :param state: User's state
    """

    state_data = await state.get_data()

    captcha_data = callback.data[16:].split("_")
    captcha_id = captcha_data[0]
    captcha_text = captcha_data[1]

    if state_data.get("captcha_id") is None or \
            captcha_id != str(state_data["captcha_id"]):
        await callback.answer(
            TextFormatter(
                "error:outdatedcaptcha",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    if captcha_text == state_data["captcha_text"]:
        await callback.message.delete()

        UserLog(
            callback.from_user.id,
            attempt=state_data["captcha_attempt"]
        ).log("Passed captcha with")

        await state.clear()
        await state.set_state(ReffedUserState.MENU)
        await User(callback.from_user.id).update(captcha_passed=True)

        logger.info(f"User have passed the captcha: {callback.from_user.id}")

        await send_channel_link(
            callback.message,
            lang_code=callback.from_user.language_code
        )
        await callback.answer(
            TextFormatter(
                "captcha:success",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    # There are 2 attempts
    # but "captcha_attempt" is starting from 0, so we have 1 here
    if state_data["captcha_attempt"] >= 1:
        await state.clear()

        await callback.answer(
            TextFormatter(
                "error:captcha_too_many_attempts",
                callback.from_user.language_code
            ).text,
            True
        )

        await callback.message.delete()
        await start_captcha_process(
            callback.message,
            state,
            callback.from_user.language_code
        )
        return

    UserLog(callback.from_user.id, attempt=state_data["captcha_attempt"]).log(
        "Can't pass the captcha"
    )

    state_data["captcha_attempt"] += 1
    await state.set_data(state_data)

    await callback.answer(
        TextFormatter(
            "error:captcha_failed",
            callback.from_user.language_code
        ).text,
        True
    )


@router.message(CaptchaState.CAPTCHA)
async def captcha_message_handler(
    message: Message,
    state: FSMContext
) -> None:
    """
    All the message handler in captcha

    :param message: Telegram message
    :param state: User's state
    """

    await send_captcha_message(message, state)
