from loguru import logger
from aiogram.enums import ChatMemberStatus
from aiogram.types import (
    Message,
    ChatMemberUpdated
)
from aiogram import (
    F,
    Router
)

from .config import (
    Cache,
    Config
)


router = Router()
router.chat_member(F.chat.id == Config.CHANNEL_ID)


@router.chat_member(F.new_chat_member.status == ChatMemberStatus.LEFT)
async def channel_member_left_observer(member: ChatMemberUpdated) -> None:
    """
    Obsever for left / banned from channel events

    :param member: Updated member data
    """

    # TODO remove from DB>.subscribed = False rn
    # TODO Remove from local channel list. for user.
    ...


@router.channel_post(F.new_chat_title)
async def channel_title_observer(channel_post: Message) -> None:
    """
    Checking title changes

    :param channel_post: Telegram message
    """

    Cache.chat_title = channel_post.chat.title
    logger.info(f"New chat title: {Cache.chat_title}")


@router.chat_member(F.new_chat_member.status == ChatMemberStatus.MEMBER)
async def channel_member_observer(member: ChatMemberUpdated) -> None:
    """
    """

    # TODO обновлять - теперь он subscriberd
    # нужен dispattcher чтобы сменить staete на default и по поводу set_data хз
    ...
