import functools

from ..database import User
from ..states import ReffedUserState


class ReffedUserVerification:
    """
    Checking whether user is reffed by someone

    Then he got another kind of menu. Only if he don't have has_link
    """

    @staticmethod
    def check(function) -> callable:
        """
        Decorator for checking whether user is reffed by someone
        and don't has_link

        Changes User's state to ReffedUserState, if True
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

                if user and user.joined_by_user_id is not None \
                        and not user.has_link:
                    await kwargs["state"].set_state(ReffedUserState.MENU)
                    return

            return await function(*args, **kwargs)
        return wrapped
