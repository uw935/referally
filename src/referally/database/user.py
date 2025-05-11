import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    insert
)

from .models import UserModel
from .session import connection


class User:
    """
    Class for working with database' user    
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
        username: str = None,
        joined_by_user_id: int = None,
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
