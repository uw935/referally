import os
import sys
from loguru import logger
from dotenv import (
    load_dotenv,
    find_dotenv
)


LOGGER_FORMAT: str = (
    "<green>[{time}][{level}][{extra[source]}]</green>: "
    "<level>{message}</level> (line: {line})"
)


logger.remove()
logger.configure(
    extra={
        "source": "Bot"
    }
)
logger.add(
    sink=sys.stdout,
    level="INFO",
    colorize=True,
    format=LOGGER_FORMAT,
    catch=True
)
logger.add(
    sink="./logs/bot.log",
    level="INFO",
    rotation="1 MB",
    format=LOGGER_FORMAT,
    compression="zip",
    delay=True,
    catch=True
)


load_dotenv(
    find_dotenv(
        ".env",
        True
    ),
    override=True
)


class Config:
    """
    Const variables
    """

    BOT_TOKEN: str = os.environ["BOT_TOKEN"]
    ADMIN_ID: int = int(os.environ["TELEGRAM_ADMIN_ID"])
    DEFAULT_LANG: str = os.environ["DEFAULT_LANG"].lower()
    CAROUSEL_LIMIT: int = 5

    # This variable will be counted with start
    # and never changes
    bot_username: str = None
