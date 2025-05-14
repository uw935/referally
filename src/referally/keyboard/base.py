import math
from abc import (
    ABC,
    abstractmethod
)

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from ..config import Config
from ..texts import TextFormatter
from .methods import (
    create_markup,
    create_button
)


class Keyboard(ABC):
    """
    Base class of keyboard
    """

    def __init__(self, lang_code: str = Config.DEFAULT_LANG) -> None:
        """
        Initialization

        :param lang_code: Language code of keyboard's text that is needed
        """

        self.lang_code = lang_code

    @property
    @abstractmethod
    def markup(self) -> InlineKeyboardMarkup:
        """
        Property for getting markup

        :return: Markup ready-to-use
        """

        pass


class PaginationKeyboard(Keyboard):
    """
    Pagination keyboard

    There are provided `buttons (in initialization)`
    with `sliders` and `Back` button
    """

    def __init__(
        self,
        lang_code: str,
        buttons: tuple[InlineKeyboardButton] | list[InlineKeyboardButton],
        callback: CallbackQuery,
        current_page: int,
        objects_count: int,
        buttons_limit: int = Config.CAROUSEL_LIMIT
    ) -> None:
        """
        Creating Pagination Keyboard with sliders and back button

        :param lang_code: Language code of keyboard' text needed
        :param buttons: Tuple or list of buttons to display on this page
        :param callback: Page display callback. See `more about` it below
        :param current_page: Current page index (will be display in buttons)
        :param objects_count: All the objects to paginate count
        (will be display in buttons)
        :param buttons_limit: Maximum count of objects on one page. Optional
        :return: Pagination keyboard

        ## More about `callback`
        Callback will receive index of page that is needed to display
        after "_"

        Example
            1. **CALLBACK_HANDLER_1** — have "_1" at the end
            which references to current page to display
        """

        self.lang_code = lang_code
        self.buttons = buttons
        self.callback = callback
        self.current_page = current_page
        self.all_pages = math.ceil(objects_count / buttons_limit)

    @property
    def markup(self) -> InlineKeyboardMarkup:
        previous_page = self.current_page - 1
        next_page = self.current_page + 1

        if self.all_pages <= 0:
            self.all_pages = 1

        if previous_page < 0:
            previous_page = self.all_pages - 1

        if next_page >= self.all_pages:
            next_page = 0

        return create_markup(
            *self.buttons,
            (
                create_button(
                    TextFormatter(
                        "keyboard:list:back",
                        self.lang_code
                    ).text,
                    f"{self.callback}{previous_page}"
                    if self.all_pages > 1 else "DO_NOTHING"
                ),
                create_button(
                    f"{self.current_page + 1} / {self.all_pages}",
                    "DO_NOTHING"
                ),
                create_button(
                    TextFormatter(
                        "keyboard:list:forward",
                        self.lang_code
                    ).text,
                    f"{self.callback}{next_page}"
                    if self.all_pages > 1 else "DO_NOTHING"
                )
            ),
            (
                create_button(
                    TextFormatter(
                        "keyboard:back",
                        self.lang_code
                    ).text,
                    "BACK"
                ),
            )
        )


class BackKeyboard(Keyboard):
    """
    Base back keyboard markup

    There is only one `Back` button
    """

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
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


class AboutKeyboard(Keyboard):
    """
    About keyboard

    There is only one `About this project` button
    """

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return create_markup(
            (
                create_button(
                    TextFormatter(
                        "keyboard:about",
                        self.lang_code
                    ).text,
                    # See why in keyboard/admin.py
                    url="https://t.me/+FOsRd3bAe7o3YzFi"
                ),
            ),
        )
