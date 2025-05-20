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
    Observer that is watching for channel' events with members

    Remove / Kicked / Added

    :param member: Telegram chat member
    :param dispatcher: Current dispatcher instance
    """

    user = await User(member.from_user.id).get()

    if user is None:
        return

    if member.new_chat_member.status == ChatMemberStatus.MEMBER:
        logger.info(f"New user just subscribed: {member.from_user.id}")
    else:
        logger.info(f"New user just unsubscribed: {member.from_user.id}")

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

    if user.joined_by_user_id is not None and user.captcha_passed:
        if member.new_chat_member.status == ChatMemberStatus.MEMBER:
            await User(user.joined_by_user_id).update(plus_referal_count=1)

            await dispatcher.fsm.get_context(
                member.bot,
                int(member.from_user.id),
                int(member.from_user.id)
            ).clear()

            await member.bot.send_message(
                member.from_user.id,
                TextFormatter(
                    "refd_user:subscribed",
                    member.from_user.language_code
                ).text
            )

            await send_menu_message(member, from_bot=True)
            return

        # If bot didn't catch his subscription
        # it seems user subscribed when he didn't passed the captcha
        if not user.subscribed:
            return

        await User(user.joined_by_user_id).update(plus_referal_count=-1)
