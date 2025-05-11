import functools
from aiogram.types import User

from ..config import Config
from ..states import AdminState
from ..texts import TextFormatter


class AdminVerification:
    """
    Admin verification
    """

    @staticmethod
    def check() -> callable:
        """
        Decorator for checking whether user is admin

        Changes User's state to another, if True
        """

        def wrapper(func) -> callable:
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                if args[0] is not None:
                    user: User = args[0].from_user

                    if user.id == Config.ADMIN_ID:
                        await kwargs["state"].set_state(AdminState.MENU)
                        await args[0].answer(
                            TextFormatter(
                                "error:no_state",
                                user.language_code
                            ).text
                        )
                        return

                return await func(*args, **kwargs)
            return wrapped
        return wrapper
