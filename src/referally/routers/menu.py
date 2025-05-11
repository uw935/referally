from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.command import (
    CommandStart,
    CommandObject
)
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram import (
    F,
    Router
)

from ..database import User
from ..texts import TextFormatter
from .user import menu as user_menu
from .admin import panel as admin_panel
from ..verification import AdminVerification
from ..config import (
    Cache,
    Config
)
from .refd_user import (
    captcha,
    menu as refd_user_menu,
    router as refd_user_router
)


router = Router()
router.include_router(admin_panel.router)
router.include_router(refd_user_router)


@router.callback_query(F.data == "DO_NOTHING")
async def do_nothing_callback_handler(_: CallbackQuery) -> None:
    """
    Callback for buttons, just do nothing

    For example, pagination
    """

    return


@router.message(default_state, CommandStart())
@AdminVerification.check()
async def start_handler(
    message: Message,
    state: FSMContext,
    command: CommandObject = None
) -> None:
    """
    /start command handler

    :param message: Telegram Message
    :param state: User's state. Needed for check @decorator
    :param command: Telegram command
    """

    user = await User(message.from_user.id).get()

    if command.args is not None and command.args.isdigit() or\
            user and user.has_link is False:
        if command.args and message.from_user.id == int(command.args):
            if user and user.has_link:
                await message.answer(
                    TextFormatter(
                        "error:join_yourself",
                        message.from_user.language_code
                    ).text
                )
                await user_menu.send_menu_message(message)
                return
        else:
            if user is not None:
                if user.subscribed:
                    if user.has_link is False:
                        await message.answer(
                            TextFormatter(
                                "refd_user:can_ref",
                                message.from_user.language_code
                            ).text
                        )
                        # TODO менять ему has_link
                        await user_menu.send_menu_message(message)
                        return

                    await message.answer(
                        TextFormatter(
                            "user:already_signed",
                            message.from_user.language_code
                        ).text
                    )
                    await user_menu.send_menu_message(message)
                    return

                if user.captcha_passed:
                    await refd_user_menu.send_channel_link(message, state)
                    return
            else:
                await User(message.from_user.id).add(
                    username=message.from_user.username,
                    joined_by_user_id=int(command.args)
                )
                # TODO checks if he didn't created.. what's next?nadaещё тогда пробовать
                # TODO write to admin(s)(? admins in the future)
                # TODO write that here is new user there that was refed

            await message.answer(
                TextFormatter(
                    "refd_user:start",
                    message.from_user.language_code,
                    channel_name=Cache.chat_title
                ).text
            )
            await captcha.start_captcha_process(message, state)
            return

    is_member = await message.bot.get_chat_member(
        Config.CHANNEL_ID,
        message.from_user.id
    )

    is_member = not (
        is_member.status == ChatMemberStatus.LEFT
        or is_member.status == ChatMemberStatus.KICKED
    )

    if user is None:
        await User(message.from_user.id).add(
            has_link=True,
            subscribed=is_member,
            username=message.from_user.username
        )
        await message.answer(
            TextFormatter(
                "user:start",
                message.from_user.language_code
            ).text
        )

    if is_member is False:
        await user_menu.send_channel_subscribe(message)
        return

    await user_menu.send_menu_message(message)


@router.message(default_state)
@AdminVerification.check()
async def message_handler(
    message: Message,
    state: FSMContext
) -> None:
    """
    All the messages handler

    :param message: Telegram message
    :param state: User's state. Needed for check @decorator
    """

    await user_menu.send_menu_message(message)
