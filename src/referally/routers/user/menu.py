from aiogram.types import Message

from ...config import Cache
from ...texts import TextFormatter
from ...keyboard import (
    AboutKeyboard,
    SubscribeKeyboard
)


async def send_menu_message(
    message: Message,
    is_edit: bool = False
) -> None:
    """
    Send default menu message for users

    :param message: Telegram message
    :param is_edit: Whether this message should be edited
    """

    text = TextFormatter(
        "user:menu",
        message.from_user.language_code,
        ref_link=f"https://t.me/{Cache.bot_username}"
        f"?start={message.from_user.id}",
        rating_number=1,
        users=20
    ).text

    reply_markup = AboutKeyboard(
        message.from_user.language_code
    ).markup

    if is_edit:
        await message.edit_text(text, reply_markup=reply_markup)
        return

    await message.answer(text, reply_markup=reply_markup)


async def send_channel_subscribe(message: Message) -> None:
    """
    Send message with subscription require

    :param message: Telegram message
    """

    await message.answer(
        TextFormatter(
            "user:subscription_require",
            message.from_user.language_code
        ).text,
        reply_markup=SubscribeKeyboard(
            message.from_user.language_code
        ).markup
    )
