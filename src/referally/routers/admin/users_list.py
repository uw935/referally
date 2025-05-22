from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram import (
    F,
    Router
)

from ...config import Config
from ...texts import TextFormatter
from ...database import (
    User,
    AllUsers,
    UserCount,
    UserRating
)
from ...keyboard import (
    create_button,
    PaginationKeyboard,
    AdminUserListKeyboard
)


router = Router()


@router.callback_query(F.data[:11] == "USERS_LIST_")
async def users_list_callback_handler(callback: CallbackQuery) -> None:
    """
    Users List callback handler

    :param callback: Telegram callback
    """

    users_count = await UserCount.get()
    users = await AllUsers.get(
        Config.CAROUSEL_LIMIT,
        # Offset moving with every page by carousel limit
        int(callback.data[11:]) * Config.CAROUSEL_LIMIT
    )

    buttons = [
        (
            create_button(
                TextFormatter(
                    "keyboard:user_button",
                    callback.from_user.language_code,
                    user_id=user.user_id
                ).text,
                f"USER_VIEW_{callback.data[11:]}_{user.user_id}"
            ),
        )
        for user in users
    ]

    await callback.message.edit_text(
        TextFormatter(
            "admin:users_list:text",
            callback.from_user.language_code,
            users_count=users_count
        ).text,
        reply_markup=PaginationKeyboard(
            callback.from_user.language_code,
            buttons,
            "USERS_LIST_",
            int(callback.data[11:]),
            users_count
        ).markup
    )


@router.callback_query(F.data[:11] == "USER_UNBAN_")
@router.callback_query(F.data[:9] == "USER_BAN_")
async def block_callback_handler(callback: CallbackQuery) -> None:
    """
    Actions with user's liberty

    :param callback: Telegram callback
    """

    callback_data = callback.data.split("_")
    user_id = int(callback_data[2])

    if user_id == callback.from_user.id:
        await callback.answer(
            TextFormatter(
                "error:cant_block_yourself",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    user = await User(user_id).get()

    if user is None:
        await callback.answer(
            TextFormatter(
                "error:user_not_found",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    await User(user_id).update(
        blocked="UNBAN" not in callback.data
    )

    await callback.message.edit_reply_markup(
        reply_markup=AdminUserListKeyboard(
            user_id,
            "UNBAN" not in callback.data,
            callback.from_user.id
        ).markup
    )

    await callback.answer(
        TextFormatter(
            f"admin:{callback_data[1].lower()}ned",
            callback.from_user.id
        ).text,
        True
    )


@router.callback_query(F.data[:10] == "USER_VIEW_")
async def user_info_callback_handler(callback: CallbackQuery) -> None:
    """
    User information panel callback handler

    :param callback: Telegram callback
    """

    callback_data = callback.data[10:].split("_")

    users_list_back_index = callback_data[0]
    user_id = int(callback_data[1])

    user = await User(user_id).get()

    if user is None:
        await callback.answer(
            TextFormatter(
                "error:user_not_found",
                callback.from_user.language_code
            ).text,
            True
        )
        return

    yes_text = TextFormatter(
        "admin:yes",
        callback.from_user.language_code
    ).text

    no_text = TextFormatter(
        "admin:no",
        callback.from_user.language_code
    ).text

    rating = await UserRating.get(user.user_id)

    await callback.message.edit_text(
        TextFormatter(
            "admin:user_view:text",
            callback.from_user.language_code,
            user_id=user.id,
            tgid=user.user_id,
            rating=rating,
            username=f"@{user.username}" if user.username else no_text,
            reg_timestamp=datetime.fromtimestamp(user.created_at)
            .strftime("%d.%m.%y %H:%M"),
            was_refered=yes_text if user.joined_by_user_id is not None
            else no_text,
            has_link=yes_text if user.has_link else no_text,
            referals_count=user.referals_count,
            is_subscribed=yes_text if user.subscribed else no_text
        ).text,
        reply_markup=AdminUserListKeyboard(
            user_id,
            user.blocked,
            callback.from_user.language_code,
            users_list_back_index
        ).markup
    )
