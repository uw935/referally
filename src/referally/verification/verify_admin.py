import functools
from aiogram.types import User

from ..config import Config
from ..states import AdminState


class AdminVerification:
    """
    Admin verification
    """

    @staticmethod
    def check() -> callable:
        """
        Decorator for checking whether user is adamin
        """

        def wrapper(func) -> callable:
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                if args[0] is not None:
                    user: User = args[0].from_user

                    # If there is no state
                    # then just leave
                    if "state" not in kwargs.keys():
                        return

                    if user.id == Config.ADMIN_ID:
                        await kwargs["state"].set_state(AdminState.MENU)
                        return

                return await func(*args, **kwargs)
            return wrapped
        return wrapper
