from aiogram.types import InlineKeyboardMarkup

from .base import Keyboard
from ..texts import TextFormatter
from .methods import (
    create_markup,
    create_button
)


class AdminUserListKeyboard(Keyboard):
    """
    Administrator Users List keyboard

    There are `Ban` and `Back` buttons in here
    """

    def __init__(
        self,
        user_id: int | str,
        is_blocked: bool,
        lang_code: str,
        back_index: int | str = 0
    ) -> None:
        """
        Initialization of Users List keyboard

        :param user_id: Telegram user ID
        :param is_blocked: True if user is blocked from the bot
        :param lang_code: User's language code
        :param back_index: Index for returning back to UsersList menu
        """

        self.user_id = user_id
        self.block_or_unblock = "unban" if is_blocked else "ban"
        self.lang_code = lang_code
        self.back_index = back_index

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
            (
                create_button(
                    TextFormatter(
                        f"keyboard:{self.block_or_unblock}",
                        self.lang_code
                    ).text,
                    f"USER_{self.block_or_unblock.upper()}_{self.user_id}"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:back",
                        self.lang_code
                    ).text,
                    f"USERS_LIST_{self.back_index}"
                ),
            ),
        )


class AdminMenuKeyboard(Keyboard):
    """
    Administaror Main Menu keyboard

    There are `Statistics`, `Users List` and `About` buttons here
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
                    "ADMIN_STATISTICS"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:users_list",
                        self.lang_code
                    ).text,
                    "USERS_LIST_0"
                ),
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:about",
                        self.lang_code
                    ).text,
                    # Anti-zpizdit' & change copyrights (that why it's not const)
                    # i know it's easy to find, but at least..
                    url="https://github.com/uw935/referallyi"
                ),
            )
        )
