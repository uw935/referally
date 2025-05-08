from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.command import CommandStart
from aiogram import (
    F,
    Router
)

from .admin import panel
from ..states import AdminState
from ..texts import TextFormatter
from ..verification import AdminVerification


router = Router()
router.include_router(panel.router)

router.callback_query.filter(AdminState.MENU)


@router.callback_query(F.data == "DO_NOTHING")
async def do_nothing_callback_handler(_: CallbackQuery) -> None:
    """
    Callback for buttons, just do nothing

    For example, pagination
    """

    return


# State isn't used in function and seems useless
# however here and in "message_handler" it used only for decorator
# no, there aren't any options to avoid this
@router.message(default_state, CommandStart())
@AdminVerification.check()
async def start_handler(
    message: Message,
    state: FSMContext
) -> None:
    """
    /start command handler

    :param message: Telegram Message
    :param state: User's state. Needed for check @decorator
    """

    await message.answer("Hello hi")


@router.message(default_state)
@AdminVerification.check()
async def message_handler(
    message: Message,
    state: FSMContext
) -> None:
    """
    All the messages handler

    :param message: Telegram message
    :param state: User's state. Needed for check @decorator
    """

    await message.answer("Hi")
