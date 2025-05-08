from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def create_button(
    text: str,
    callback: str = None,
    url: str = None
) -> InlineKeyboardButton:
    """
    Create inline keyboard button

    :param text: Button text
    :param callback: Button callback. Optional
    :param url: URL Button. Optional
    :return: Inline keyboard button
    """

    return InlineKeyboardButton(
        text=text,
        callback_data=callback,
        url=url
    )


def create_markup(*args: tuple[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    """
    Create inline keyboards

    :param buttons: List of inline keyboard buttons
    :return: Inline keyboard markup
    """

    return InlineKeyboardMarkup(inline_keyboard=args)
