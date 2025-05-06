from aiogram.types import CallbackQuery 
from aiogram import (
    F,
    Router
)

from ...texts import TextFormatter
from ...keyboard import (
    BackKeyboard,
    PaginationKeyboard
)


router = Router()


@router.callback_query(F.data[:11] == "USERS_LIST_")
async def users_list_callback_handler(callback: CallbackQuery) -> None:
    """
    Users List callback handler

    :param callback: Telegram callback
    """

    users_count = 1

    buttons = (...)

    await callback.message.edit_text(
        TextFormatter(
            "admin:users_list:text",
            callback.from_user.language_code,
            count=users_count
        ).text,
        reply_markup=PaginationKeyboard(
            callback.from_user.language_code,
            buttons,
            "USERS_LIST_",
            callback.data[11:],
            3
        )
    )
