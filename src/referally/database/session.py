import functools

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

from ..config import Config


engine = create_async_engine(Config.DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connection(function: callable) -> callable:
    """
    Decorator for session connection

    :param function: Decorated function
    """

    @functools.wraps(function)
    async def wrapper(*args, **kwargs) -> callable:
        """
        Decorator wrapper

        :param args: Function's arguments
        :param kwargs: Function's key-worded arguments
        :return: Given function
        """

        async with async_session_maker() as session:
            try:
                return await function(*args, _db_session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
