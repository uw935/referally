from aiogram.types import InlineKeyboardMarkup

from ..config import Cache
from .base import Keyboard
from ..texts import TextFormatter
from .methods import (
    create_markup,
    create_button
)


class SubscribeKeyboard(Keyboard):
    """
    Base back keyboard markup
    """

    def __init__(self, lang_code: str, link: str = Cache.chat_invite_link) -> None:
        """
        Initialization of subscribe keyboard

        :param link: Link to subscribe
        :param lang_code: User's language code
        """

        self.link = link
        self.lang_code = lang_code

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
            (
                create_button(
                    TextFormatter(
                        "keyboard:subscribe",
                        self.lang_code
                    ).text,
                    url=self.link
                ),
            ),
        )
