import math
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from abc import (
    ABC,
    abstractmethod
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
        
        :param lang_code: Language of keyboard that needed
        """

        self.lang_code = lang_code

    @property
    @abstractmethod
    def markup(self) -> InlineKeyboardMarkup:
        """
        Get markup
        
        :return: Markup ready-to-use
        """

        pass


class PaginationKeyboard(Keyboard):
    """
    Base pagination keyboard
    """

    def __init__(
        self,
        lang_code: str,
        buttons: tuple[InlineKeyboardButton] | list[InlineKeyboardButton],
        callback: str,
        current_page: int,
        objects_count: int,
        page_limit: int = Config.CAROUSEL_LIMIT
    ) -> None:
        """
        Initialization of Pagination keyboard

        :param lang_code: Language code
        :param buttons: Tuple or list of buttons to display on this page
        :param callback: Next page callback
        :param current_page: Current page count
        :param objects_count: All the objects count
        :param page_limit: Pages limit (how much objects on one page)
        :return: Pagination keyboard
        """

        self.lang_code = lang_code
        self.buttons = buttons
        self.callback = callback
        self.current_page = current_page
        self.objects_count = objects_count
        self.page_limit = page_limit

    @property
    def markup(self) -> InlineKeyboardMarkup:
        all_pages = math.ceil(self.objects_count / self.page_limit)

        previous_page = self.current_page - 1
        next_page = self.current_page + 1

        if all_pages <= 0:
            all_pages = 1

        if previous_page < 0:
            previous_page = all_pages - 1

        if next_page >= all_pages:
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
                    if all_pages > 1 else "DO_NOTHING"
                ),
                create_button(
                    f"{self.current_page + 1} / {all_pages}",
                    "DO_NOTHING"
                ),
                create_button(
                    TextFormatter(
                        "keyboard:list:forward",
                        self.lang_code
                    ).text,
                    f"{self.callback}{next_page}"
                    if all_pages > 1 else "DO_NOTHING"
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
