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
