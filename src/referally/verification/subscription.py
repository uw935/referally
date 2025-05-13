import functools

from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

from ..config import Config
from ..texts import TextFormatter
from ..keyboard import SubscribeKeyboard


class SubscriptionVerification:
    """
    Checking for subscription on channel
    """

    @staticmethod
    def check(function: callable) -> callable:
        """
        Check whether user subscribed to the channel

        :param function: Decorator's function
        :return: Wrapper function
        """

        @functools.wraps(function)
        async def wrapper(*args, **kwargs) -> None:
            """
            Wrapper for decorator

            :param args: Function's positional arguments
            :param kwargs: Function's key-worded arguments
            """

            if args[0] is not None:
                user_subscribed = await args[0].bot.get_chat_member(
                    Config.CHANNEL_ID,
                    args[0].from_user.id
                )

                user_subscribed = not (
                    user_subscribed.status == ChatMemberStatus.LEFT
                    or user_subscribed.status == ChatMemberStatus.KICKED
                )

                answer_function = (
                    args[0].answer
                    if isinstance(args[0], Message)
                    else args[0].message.answer
                )

                if user_subscribed is False:
                    await answer_function(
                        TextFormatter(
                            "user:subscription_require",
                            args[0].from_user.language_code
                        ).text,
                        reply_markup=SubscribeKeyboard(
                            args[0].from_user.language_code
                        ).markup
                    )
                    return

            return await function(*args, **kwargs)
        return wrapper
