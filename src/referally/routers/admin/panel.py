from aiogram import Router
from aiogram.types import Message

from ...keyboard import *
from ...texts import TextFormatter


router = Router()


async def send_menu_message(
    message: Message,
    is_edit: bool = False
) -> None:
    """
    Send default menu message

    :param message: Telegram message
    :param is_edit: Whether this message should be edited
    """

    text = TextFormatter("admin:menu", message.from_user.language_code).text

    if is_edit:
        await message.edit_text(
            text,
            reply_markup=create_markup(
                [
                    create_markup(
                        TextFormatter(
                            "keyboard:statistics",
                            message.from_user.language_code
                        ),
                        "STATISTICS"
                    )
                ],
                [
                    create_markup(
                        TextFormatter(
                            "keyboard:users_list",
                            message.from_user.language_code
                        ),
                        "USERS_LIST"
                    )
                ],
                [
                    create_markup(
                        TextFormatter(
                            "keyboard:settings",
                            message.from_user.language_code
                        ),
                        "SETTINGS"
                    )
                ]
            )
        )
