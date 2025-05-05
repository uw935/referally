from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.command import CommandStart
from aiogram import (
    F,
    Router
)

from ..config import Config
from ..states import AdminState
from ..texts import TextFormatter
from .admin import panel


router = Router()
router.include_router(panel.router)


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

    if message.from_user.id == Config.ADMIN_ID:
        await state.set_state(AdminState)
        await panel.send_menu_message()
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
