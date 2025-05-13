from aiogram.types import CallbackQuery
from aiogram import (
    F,
    Router
)

from ...texts import TextFormatter
from ...keyboard import BackKeyboard
from ...database import (
    UserModel,
    UserCount,
    UserRating
)


router = Router()


@router.callback_query(F.data == "ADMIN_STATISTICS")
async def admin_statistics_handler(callback: CallbackQuery) -> None:
    """
    Handler of admin statistics query

    :param callback: Telegram Callback
    """

    users_count = await UserCount.get()
    new_subscribers = await UserCount.get(
        (
            UserModel.subscribed.is_(True),
            UserModel.joined_by_user_id.is_not(None)
        )
    )

    top_users = await UserRating.get_top(3)
    users_rating = ""

    for user in top_users:
        mention = f"@{user.username}"

        if user.username is None:
            text = TextFormatter(
                "keyboard:open_profile",
                callback.from_user.id
            ).text

            mention = f"[{text}](tg://user?id={user.user_id})"

        users_rating += f"{top_users.index(user) + 1}\\. {mention} "
        users_rating += f"\\(\\+{user.referals_count}\\)\n"

    await callback.message.edit_text(
        TextFormatter(
            "admin:statistics",
            callback.from_user.language_code,
            True,
            users_count=users_count,
            new_subscribers=new_subscribers,
            users_rating=users_rating
        ).text,
        reply_markup=BackKeyboard(
            callback.from_user.language_code
        ).markup
    )
