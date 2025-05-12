import functools

from ..database import User
from ..texts import TextFormatter


class BlockedVerification:
    """
    Checking whether user is reffed by someone

    Then he got another kind of menu. Check out documentation for more.
    """

    @staticmethod
    def check(function) -> callable:
        """
        Decorator for checking whether user is reffed by someone
        and don't has_link

        Changes User's state to another, if True
        """

        @functools.wraps(function)
        async def wrapped(*args, **kwargs):
            """
            Wrapper for decorated function

            :param args: Function's arguments
            :param kwargs: Key-worded arguments            
            """

            if args[0] is not None:
                user = await User(args[0].from_user.id).get()

                if user.blocked:
                    await args[0].answer(
                        TextFormatter(
                            "error:block",
                            args[0].from_user.language_code
                        ).text
                    )
                    return

            return await function(*args, **kwargs)
        return wrapped
