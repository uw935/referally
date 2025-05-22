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
    Subscription keyboard

    There is only one `Subscribe` button
    """

    def __init__(self, lang_code: str, link: str | None = None) -> None:
        """
        Initialization of subscribe keyboard

        :param lang_code: Language code of keyboard's text
        :param link: Link to subscribe. Optional.
        Defaults to `Cache.chat_invite_link`
        """

        self.link = link or Cache.chat_invite_link
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
