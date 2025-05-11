from loguru import logger
from aiogram.enums import ChatMemberStatus
from aiogram.types import (
    Message,
    ChatMemberUpdated
)
from aiogram import (
    F,
    Router,
    Dispatcher
)

from .database import User
from .texts import TextFormatter
from .routers.user.menu import send_menu_message
from .config import (
    Cache,
    Config
)


router = Router()
router.chat_member(F.chat.id == Config.CHANNEL_ID)


@router.channel_post(F.new_chat_title)
async def channel_title_observer(channel_post: Message) -> None:
    """
    Checking title changes

    :param channel_post: Telegram message
    """

    Cache.chat_title = channel_post.chat.title
    logger.info(f"New chat title: {Cache.chat_title}")


@router.chat_member(F.new_chat_member.status == ChatMemberStatus.LEFT)
@router.chat_member(F.new_chat_member.status == ChatMemberStatus.KICKED)
@router.chat_member(F.new_chat_member.status == ChatMemberStatus.MEMBER)
async def channel_member_observer(
    member: ChatMemberUpdated,
    dispatcher: Dispatcher
) -> None:
    """
    Observer that is watching for new members

    :param member: Telegram chat member
    :param dispatcher: Current dispatcher instance
    """

    user = await User(member.from_user.id).get()

    if user is None:
        return

    await User(member.from_user.id).update(
        subscribed=(
            member.new_chat_member.status == ChatMemberStatus.MEMBER
        ),
        has_link=(
            None
            if member.new_chat_member.status != ChatMemberStatus.MEMBER
            else True
        )
    )

    if member.new_chat_member.status == ChatMemberStatus.MEMBER:
        await dispatcher.fsm.get_context(
            member.bot,
            int(member.from_user.id),
            int(member.from_user.id)
        ).clear()

        await member.answer(
            TextFormatter(
                "refd_user:subscribed",
                member.from_user.language_code
            )
        )
        await send_menu_message(member)
