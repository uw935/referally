from aiogram import Router
from aiogram.types import Message

from ...texts import TextFormatter
from ...states import ReffedUserState
from ...keyboard import SubscribeKeyboard


router = Router()


async def send_channel_link(message: Message) -> None:
    """
    Sends link to channel

    :param message: Telegram message
    """

    await message.answer(
        TextFormatter(
            "refd_user:channel",
            message.from_user.language_code
        ).text,
        reply_markup=SubscribeKeyboard(
            "https://t.me/markenter",
            message.from_user.language_code
        ).markup
    )


@router.message(ReffedUserState.MENU)
async def reffed_user_message_handler(message: Message) -> None:
    """
    All the messages handler for reffed user

    :param message: Message
    """

    await send_channel_link(message)
