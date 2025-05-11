from aiogram import Router
from aiogram.types import Message

from ...config import Config
from ...texts import TextFormatter
from ...states import ReffedUserState
from ...keyboard import SubscribeKeyboard


router = Router()


async def send_channel_link(message: Message) -> None:
    """
    Sends link to channel

    :param message: Telegram message
    """

    channel_information = await message.bot.get_chat(Config.CHANNEL_ID)

    await message.answer(
        TextFormatter(
            "refd_user:channel",
            message.from_user.language_code
        ).text,
        reply_markup=SubscribeKeyboard(
            channel_information.invite_link,
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
