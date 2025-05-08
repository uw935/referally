from aiogram import (
    F,
    Router
)
from aiogram.types import (
    Message,
    CallbackQuery
)

from ...states import AdminState
from ...texts import TextFormatter
from ...keyboard import AdminMenuKeyboard
from . import (
    users_list,
    statistics
)


router = Router()
router.include_router(users_list.router)
router.include_router(statistics.router)


async def send_menu_message(
    message: Message,
    is_edit: bool = False
) -> None:
    """
    Send default menu message

    :param message: Telegram message
    :param is_edit: Whether this message should be edited
    """

    text = TextFormatter(
        "admin:menu",
        message.from_user.language_code,
        name=message.from_user.first_name
    ).text

    reply_markup = AdminMenuKeyboard(
        message.from_user.language_code
    ).markup

    if is_edit:
        await message.edit_text(text, reply_markup=reply_markup)
        return

    await message.answer(text, reply_markup=reply_markup)


@router.callback_query(AdminState.MENU, F.data == "BACK")
async def back_button_handler(callback: CallbackQuery) -> None:
    """
    Back button handler

    :param message: Telegram message
    """

    await send_menu_message(callback.message, True)


@router.message(AdminState.MENU)
async def admin_message_handler(message: Message) -> None:
    """
    All the messages from admin

    :param message: Telegram message
    """

    await send_menu_message(message)
