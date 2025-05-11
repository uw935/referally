from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import (
    func,
    String,
    Integer,
    Boolean,
    BigInteger
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Abstract class for models
    """

    __abstract__ = True


class UserModel(Base):
    """
    User database model
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False
    )
    username: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        default=None
    )
    joined_by_user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )
    has_link: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    captcha_passed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    referals_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    subscribed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    created_at: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
