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

from ..config import Config
from ..texts import TextFormatter
from .user import menu as user_menu
from .admin import panel as admin_panel
from ..verification import AdminVerification
from .refd_user import (
    captcha,
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

    # TODO if this and NOT has_link
    if command.args is not None and command.args.isdigit():
        if message.from_user.id == int(command.args):
            await message.answer(
                TextFormatter(
                    "error:join_yourself",
                    message.from_user.language_code
                ).text
            )
            return

        # TODO if user already in db
        # TODO if he completelynew and have args -> show captcha
        # TODO if he have joined_by and not subscribed, then change joined_by to the new
            # but if joined_by = joined_by, then showlink without any captcha
        # TODO if he have joined_by and subscribed, then show him user_menu menu and make has_link
        # TODO if he doesn't have joined_by but subscribed, then show him user_menu
        # TODO if he doesnt't have joined_by and not subscribed, then continue here

        channel_information = await message.bot.get_chat(Config.CHANNEL_ID)

        await message.answer(
            TextFormatter(
                "refd_user:start",
                message.from_user.language_code,
                channel_name=channel_information.title
            ).text
        )
        await captcha.start_captcha_process(message, state)
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
