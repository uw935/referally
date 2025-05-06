from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.command import CommandStart
from aiogram import (
    F,
    Router
)

from ..states import AdminState
from ..texts import TextFormatter
from .admin import panel


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


@router.message(default_state, CommandStart())
async def start_handler(message: Message) -> None:
    """
    /start command handler

    :param message: Telegram Message
    """

    await message.answer(
        TextFormatter(
            "admin:onboard:start",
            message.from_user.language_code
        ).text
    )


@router.message(default_state)
async def message_handler(
    message: Message,
    state: FSMContext
) -> None:
    """
    All the messages handler

    :param message: Telegram message
    :param state: User's state
    """

    await state.set_state(AdminState.MENU)
    await panel.send_menu_message(message)
