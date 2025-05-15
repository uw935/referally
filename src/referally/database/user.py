import time
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    and_,
    func,
    insert,
    select,
    update
)

from .models import UserModel
from .session import connection


class User:
    """
    Class for working with database' user

    Basic CRUD
    """

    def __init__(self, user_id: int) -> None:
        """
        Initialization of user

        :param user_id: Telegram user ID
        """

        self.user_id = user_id

    @connection
    async def get(self, _db_session: AsyncSession = None) -> UserModel:
        """
        Get all the User's data

        :return: UserModel with all the data
        """

        if self.user_id is None:
            return

        query = await _db_session.execute(
            select(UserModel)
            .where(UserModel.user_id == self.user_id)
        )

        return query.scalar_one_or_none()

    @connection
    async def add(
        self,
        subscribed: bool = False,
        has_link: bool = False,
        username: str | None = None,
        joined_by_user_id: int | None = None,
        _db_session: AsyncSession = None
    ) -> bool:
        """
        Add new user

        :param subscribed: True if user subscribed to the channel. Optional
        :param has_link: True if user have referal link. Optional
        :param username: Telegram Username. Optional
        :param joined_by_user_id: User ID of whom him was referred. Optional
        :return: True if all successful, False if user was already exist
        """

        if self.user_id is None:
            return

        current_user = await self.get()

        if current_user is not None:
            return False

        await _db_session.execute(
            insert(UserModel)
            .values(
                user_id=self.user_id,
                username=username,
                joined_by_user_id=joined_by_user_id,
                has_link=has_link,
                subscribed=subscribed,
                created_at=int(time.time())
            )
        )

        await _db_session.commit()
        return True

    @connection
    async def update(
        self,
        subscribed: bool | None = None,
        has_link: bool | None = None,
        username: str = "_none",
        captcha_passed: bool | None = None,
        blocked: bool | None = None,
        plus_referal_count: int | None = None,
        _db_session: AsyncSession = None
    ) -> None:
        """
        Update User's data

        :param subscribed: True if user subscribed to the channel
        :param has_link: True if user have his referal link
        :param username: Telegram Username
        :param captcha_passed: True if user has passed the captcha
        :param blocked: True if user blocked from the bot
        :param plus_referal_count: Plus referal count of this user

        ## More about `plus_referal_count`
        This number will be added to the current user's referals_count.

        Examples
            1. -5 will remove 5 referals from this user (because (+) + (-) = -)
            2. 5 (without sign) adds 5 referalls to this user
        """

        if self.user_id is None:
            return

        to_update = {}

        if subscribed is not None:
            to_update["subscribed"] = subscribed

        if has_link is not None:
            to_update["has_link"] = has_link

        if username != "_none":
            to_update["username"] = username

        if blocked is not None:
            to_update["blocked"] = blocked

        if captcha_passed is not None:
            to_update["captcha_passed"] = captcha_passed

        if plus_referal_count is not None:
            to_update["referals_count"] = (
                UserModel.referals_count
                + plus_referal_count
            )

        if len(to_update) <= 0:
            return

        await _db_session.execute(
            update(UserModel)
            .where(UserModel.user_id == self.user_id)
            .values(to_update)
        )

        await _db_session.commit()


class AllUsers:
    """
    Methods for working with all the Users
    """

    @staticmethod
    @connection
    async def get(
        limit: int = None,
        offset: int = None,
        _db_session: AsyncSession = None
    ) -> list[UserModel]:
        """
        Get all the users

        :param limit: Maximum users to get. Optional
        :param offset: Offset of fetching. Optional
        :return: List of UserModels
        """

        users = await _db_session.execute(
            select(UserModel)
            .order_by(UserModel.id.asc())
            .limit(limit)
            .offset(offset)
        )

        return users.scalars().all()


class UserCount:
    """
    Methods for working with all the Users count
    """

    @staticmethod
    @connection
    async def get(
        conditions: tuple = tuple(),
        _db_session: AsyncSession = None
    ) -> int:
        """
        Get current users count

        :param conditions: Conditions for filtering. Optional
        :return: Current users count

        ## More about `conditions`
        You can provide any necessary filters for fetching data
        in this argument

        Examples
            1. (UserModel.referals_count >= 200, ) will return count of users
            with referals count more than 200
        """

        count = await _db_session.execute(
            select(func.count())
            .select_from(UserModel)
            .filter(*conditions)
        )

        return count.scalar()


@dataclass(repr=True, init=True, frozen=True)
class UserRatingTop:
    """
    Dataclass for UserRatingTop

    :param user_id: Telegram user ID
    :param username: Telegram username
    :param referals_count: User's referals count
    """

    user_id: int
    username: str | None
    referals_count: int


class UserRating:
    """
    Rating and all kind of that in User

    All the users rated here by `referals_count`
    the more user have it, the higher his rating
    """

    @staticmethod
    @connection
    async def get(user_id: int, _db_session: AsyncSession) -> int:
        """
        Get user's rating

        :param user_id: Telegram user ID
        :return: User's rating
        """

        user = await _db_session.execute(
            select(
                UserModel.user_id,
                # Ranking users by UserModel.referals_count
                # and calling their position "rating_number"
                # so we can access it below in return
                func.rank()
                .over(order_by=UserModel.referals_count)
                .label("rating_number")
            )
            .where(
                and_(
                    UserModel.user_id == user_id
                    and
                    UserModel.blocked.isnot(True)
                )
            )
        )

        return user.first().rating_number

    @staticmethod
    @connection
    async def get_top(
        limit: int = 3,
        _db_session: AsyncSession = None
    ) -> list[UserRatingTop]:
        """
        Get top users

        :param limit: Maximum number of top users to be returned. Optional
        :return: List of top users with UserRatingTop dataclass
        """

        users = await _db_session.execute(
            select(
                UserModel.user_id,
                UserModel.username,
                UserModel.referals_count
            )
            .filter(UserModel.blocked.isnot(True))
            .order_by(UserModel.referals_count.desc())
            .limit(limit)
        )

        return [UserRatingTop(*result) for result in users.all()]
