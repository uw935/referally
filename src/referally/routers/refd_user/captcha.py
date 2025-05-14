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

from ...database import User
from ...captcha import Captcha
from ...texts import TextFormatter
from .menu import send_channel_link
from ...states import (
    CaptchaState,
    ReffedUserState
)


router = Router()
router.message.filter(CaptchaState.CAPTCHA)
router.callback_query.filter(CaptchaState.CAPTCHA)


async def send_captcha_message(message: Message, state: FSMContext) -> None:
    """
    Sending message with captcha in it

    :param message: Telegram message
    :param state: User's state
    """

    state_data = await state.get_data()

    if state_data.get("captcha_data") is None:
        await start_captcha_process(message, state)
        return

    message = await message.answer(
        TextFormatter(
            "captcha:text",
            message.from_user.language_code,
            element=TextFormatter(
                f"captcha:{state_data['captcha_data'].text}",
                message.from_user.language_code
            ).text
        ).text,
        reply_markup=state_data["captcha_data"].keyboard
    )


async def start_captcha_process(message: Message, state: FSMContext) -> None:
    """
    Starting captcha point

    :param message: Telegram message
    :param state: User's state
    """

    await state.set_state(CaptchaState.CAPTCHA)

    captcha = Captcha("CAPTCHA_PROCEED").generate()
    logger.info(f"Generated captcha with ID: {captcha.id}")

    await state.set_data({
        "captcha_data": captcha,
        "captcha_attempt": 0
    })

    await send_captcha_message(message, state)


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

    if state_data.get("captcha_data") is None or \
            captcha_id != str(state_data["captcha_data"].id):
        await callback.answer(
            TextFormatter(
                "error:outdatedcaptcha",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    if captcha_text == state_data["captcha_data"].text:
        await callback.message.delete()

        await state.clear()
        await state.set_state(ReffedUserState.MENU)
        await User(callback.from_user.id).update(captcha_passed=True)

        await send_channel_link(callback.message)
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
        await start_captcha_process(callback.message, state)
        return

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
