import time
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    func,
    insert,
    select,
    update,
    delete
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
        Get user's data
        """

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
        :param has_link: True if user have ref link. Optional
        :param username: Telegram username. Optional
        :param joined_by_user_id: User ID of reffered. Optional
        :return: False if user already created, True otherwise
        """

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
        subscribed: bool | None= None,
        has_link: bool | None = None,
        username: str = "_none",
        _db_session: AsyncSession = None
    ) -> None:
        """
        Update user in DB
        
        :param subscribed: True if user subscribed to the channel
        :param has_link: True if user have his referal link
        :param username: Telegram username
        """

        to_update = {}

        if subscribed is not None:
            to_update["subscribed"] = subscribed
        
        if has_link is not None:
            to_update["has_link"] = has_link

        if username != "_none":
            to_update["username"] = username

        if len(to_update) <= 0:
            return

        await _db_session.execute(
            update(UserModel)
            .where(UserModel.user_id == self.user_id)
            .values(to_update)
        )

        await _db_session.commit()

    @connection
    async def delete(self, _db_session: AsyncSession) -> None:
        """
        Delete user from DB
        """

        await _db_session(
            delete(UserModel)
            .where(UserModel.user_id == self.user_id)
        )
        await _db_session.commit()


class UserCount:
    @staticmethod
    @connection
    async def get(conditions: tuple = tuple(), _db_session: AsyncSession = None) -> int:
        """
        Get current users count

        :param conditions: Conditions for filtering. Optional
        """

        count = await _db_session.execute(
            select(func.count())
            .select_from(UserModel)
            .filter(*conditions)
        )

        return count.scalar()


class UserRatingTop:
    """
    Dataclass for UserRatingTop
    """

    user_id: int
    username: str | None

    def __init__(self, user_id: int, username: str) -> None:
        """
        Initialization
        """

        self.user_id = user_id
        self.username = username

    def __repr__(self) -> None:
        """
        Representation of UserRatingTop
        """

        return f"<{self.user_id}, {self.username}>"


class UserRating:
    """
    Rating and all kind of that in User
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
                func.rank()
                .over(order_by=UserModel.referals_count)
                .label("rating_number")
            )
            .where(UserModel.user_id == user_id)
        )

        return user.first().rating_number

    @staticmethod
    @connection
    async def get_top(top_range: int = 3, _db_session: AsyncSession = None) -> list[UserRatingTop]:
        """
        Get some users from the top of the rating

        :param top_range: How many users should return. 3 by default
        :return: List of top users
        """

        users = await _db_session.execute(
            select(
                UserModel.user_id,
                UserModel.username
            )
            .order_by(UserModel.referals_count.desc())
            .limit(top_range)
        )

        return [UserRatingTop(*result) for result in users.all()]
