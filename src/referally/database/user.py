import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
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
    async def get(self, _db_session: AsyncSession) -> UserModel:
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
