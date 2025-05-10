"""
This file defines aiogram states for Referally
"""

from aiogram.fsm.state import (
    State,
    StatesGroup
)


class AdminState(StatesGroup):
    """
    State for our dear administartors
    """

    MENU: State = State()


class ReffedUserState(StatesGroup):
    """
    State for those, who was reffered by someone
    """

    MENU: State = State()


class CaptchaState(StatesGroup):
    """
    State for Captcha
    """

    CAPTCHA: State = State()
