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
from ..verification import (
    AdminVerification,
    BlockedVerification,
    ReffedUserVerification
)
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
@AdminVerification.check
@BlockedVerification.check
async def start_handler(
    message: Message,
    state: FSMContext,
    command: CommandObject = None
) -> None:
    """
    /start command handler

    :param message: Telegram Message
    :param state: User's state. Needed for check @decorator
    :param command: Telegram command. Optional
    """

    is_member = await message.bot.get_chat_member(
        Config.CHANNEL_ID,
        message.from_user.id
    )

    is_member = not (
        is_member.status == ChatMemberStatus.LEFT
        or is_member.status == ChatMemberStatus.KICKED
    )

    command_args = command.args if command is not None else None

    user = await User(message.from_user.id).get()

    if user is None and is_member is True:
        command_args = None

    if command_args is not None and command_args.isdigit() or\
            user and user.has_link is False:
        command_args = int(command_args)

        if message.from_user.id == command_args:
            # If user exists and has_link and doin'
            # this stuff like placing his ID in link. then show him an error
            # otherwise he is smart asf, register him!
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
            refed_user = await User(command_args).get()

            if refed_user is None or refed_user.blocked:
                # Basically if refer_user blocked or doesn't exist
                # it just won't count as his refer
                command_args = None

            # If user already exists in database
            if user is not None:
                # Checking if he is subscribed to channel ()
                if is_member:
                    # If user cannot invite other users
                    # don't have he's own link
                    if user.has_link is False:
                        # Then he can invite other users now!
                        # because probably he already subscribed
                        # and there was just restart of FSM or smth
                        await User(message.from_user.id).update(
                            has_link=True
                        )
                        await message.answer(
                            TextFormatter(
                                "refd_user:can_ref",
                                message.from_user.language_code
                            ).text
                        )
                        await user_menu.send_menu_message(message)
                        return

                    # If user have link and already subscribed
                    # then he can just pass to menu
                    await message.answer(
                        TextFormatter(
                            "user:already_signed",
                            message.from_user.language_code
                        ).text
                    )
                    await user_menu.send_menu_message(message)
                    return

                # If user isn't member and he somehow appears here
                # then probably it's just FSM got cleared
                # so checking if he have passed the Captcha 
                # to not show it him again
                if user.captcha_passed:
                    await refd_user_menu.send_channel_link(message, state)
                    return
            else:
                # Creating user, it seems he's new here
                await User(message.from_user.id).add(
                    username=message.from_user.username,
                    joined_by_user_id=command_args
                )

            # If user didn't passed the captcha
            # or just first time here, then proceed to captcha
            await message.answer(
                TextFormatter(
                    "refd_user:start",
                    message.from_user.language_code,
                    channel_name=Cache.chat_title
                ).text
            )
            await captcha.start_captcha_process(message, state)
            return

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
@AdminVerification.check
@BlockedVerification.check
@ReffedUserVerification.check
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
