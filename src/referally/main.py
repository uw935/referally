import asyncio

from loguru import logger
from aiogram.enums.chat_type import ChatType
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram import (
    F,
    Bot,
    Dispatcher
)

from .texts import TextFormatter
from .routers.menu import router as menu_router
from .observers import router as observer_router
from .database import (
    User,
    AllUsers
)
from .config import (
    Cache,
    Config
)


dp = Dispatcher()


async def main() -> None:
    """
    Entry point
    """

    dp.include_router(menu_router)
    dp.include_router(observer_router)

    dp.message.filter(F.chat.type == ChatType.PRIVATE)
    dp.message.filter(F.from_user.is_bot == False)  # noqa: E712

    await dp.start_polling(
        Bot(
            Config.BOT_TOKEN,
            default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN_V2,
                link_preview_is_disabled=True
            )
        )
    )


@dp.shutdown()
async def shutdown_handler(bot: Bot) -> None:
    """
    Shutdown handler

    :param bot: Current bot instance
    """

    logger.info("Goodbye!")

    await bot.send_message(
        Config.ADMIN_ID,
        TextFormatter("admin:shutdown").text
    )


@dp.startup()
async def startup_handler(bot: Bot) -> None:
    """
    Startup handler

    :param bot: Current bot instance
    """

    bot_info = await bot.get_me()
    chat_info = await bot.get_chat(Config.CHANNEL_ID)

    assert chat_info.type == ChatType.CHANNEL, (
        "CHANNEL_ID должен быть ID канала"
    )

    Cache.chat_title = chat_info.title
    Cache.bot_username = bot_info.username
    Cache.chat_invite_link = chat_info.invite_link

    assert Cache.chat_invite_link is not None, (
        "У бота нет прав на создание ссылок в канале"
    )

    logger.info(
        "Starting to up-to-dating channel subscriptions "
        "information of the bot users"
    )

    users = await AllUsers.get()

    for user in users:
        is_member = await bot.get_chat_member(
            Config.CHANNEL_ID,
            user.user_id
        )

        is_member = not (
            is_member.status == ChatMemberStatus.LEFT
            or is_member.status == ChatMemberStatus.KICKED
        )

        if user.subscribed != is_member:
            logger.info(f"Updating old subscription user: {user.user_id}")
            await User(user.user_id).update(subscribed=is_member)

    logger.info("Updating subscription information complete")
    logger.info(f"Bot started as @{Cache.bot_username}")

    await bot.send_message(
        Config.ADMIN_ID,
        TextFormatter("admin:startup").text
    )


# Prevent from starting with another file
if __name__ == "__main__":
    asyncio.run(main())
