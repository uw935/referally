from aiogram.types import InlineKeyboardMarkup

from .base import Keyboard
from ..texts import TextFormatter
from .methods import (
    create_markup,
    create_button
)


class AdminSettingsKeyboard(Keyboard):
    """
    Administrator settings keyboard
    """

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
            (
                create_button(
                    TextFormatter(
                        "keyboard:reset_data",
                        self.lang_code
                    ).text,
                    "RESET_DATA"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:captcha_settings",
                        self.lang_code
                    ).text,
                    "CAPTCHA_SETTINGS"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:back",
                        self.lang_code
                    ).text,
                    "BACK"
                ),
            ),
        )


class AdminUserListKeyboard(Keyboard):
    """
    Admin users list keyboard
    """

    def __init__():
        ...

class AdminMenuKeyboard(Keyboard):
    """
    Administaror menu keyboard
    """

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
            (
                create_button(
                    TextFormatter(
                        "keyboard:statistics",
                        self.lang_code
                    ).text,
                    "STATISTICS"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:users_list",
                        self.lang_code
                    ).text,
                    "USERS_LIST"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:copyrights",
                        self.lang_code
                    ).text,
                    url="https://t.me/+FOsRd3bAe7o3YzFi"
                ),
                create_button(
                    TextFormatter(
                        "keyboard:github",
                        self.lang_code
                    ).text,
                    url="https://github.com/uw935/referally/"
                ),
            ),
        )
