from aiogram.types import CallbackQuery
from aiogram import (
    F,
    Router
)

from ...texts import TextFormatter
from ...keyboard import BackKeyboard


router = Router()


@router.callback_query(F.data == "ADMIN_STATISTICS")
async def admin_statistics_handler(callback: CallbackQuery) -> None:
    """
    Handler of admin statistics query

    :param callback: Telegram Callback
    """

    users_count = 1
    new_subscribers = 2
    users_rating = "1 @uw935\n2 @anywonq\n3 @durov"

    await callback.message.edit_text(
        TextFormatter(
            "admin:statistics",
            callback.from_user.language_code,
            users_count=users_count,
            new_subscribers=new_subscribers,
            users_rating=users_rating
        ).text,
        reply_markup=BackKeyboard(
            callback.from_user.language_code
        ).markup
    )
