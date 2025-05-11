import functools
from aiogram.types import User

from ..states import UserReffedState


class ReffedUserVerification:
    """
    Checking whether user is reffed by someone

    Then he got another kind of menu. Check out documentation for more.
    """

    @staticmethod
    def check() -> callable:
        """
        Decorator for checking whether user is reffed by someone
        and don't has_link

        Changes User's state to another, if True
        """

        def wrapper(func) -> callable:
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                if args[0] is not None:
                    user: User = args[0].from_user

                    # TODO some checks, when there'll be DB
                    # TODO check whether has_link is not None
                    # TODO check if joined_by
                    if user is user:  # lol, just for now
                        await kwargs["state"].set_state(UserReffedState.MENU)
                        return

                return await func(*args, **kwargs)
            return wrapped
        return wrapper
