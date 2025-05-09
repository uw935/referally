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

from .user import menu
from .admin import panel
from ..states import AdminState
from ..texts import TextFormatter
from ..verification import AdminVerification


router = Router()
router.include_router(panel.router)

router.callback_query.filter(AdminState.MENU)


@router.callback_query(F.data == "DO_NOTHING")
async def do_nothing_callback_handler(_: CallbackQuery) -> None:
    """
    Callback for buttons, just do nothing

    For example, pagination
    """

    return


# @router.message(default_state, CommandStart(deep_link=True))
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

    # TODO проверка на существование в базе, если нет - отправлять смс об этом
    # TODO проверка подписки на канал в двух кейсах. без разницы.
    # TODO причем это нужно сделать на уровне мидлваровб

    if command.args is not None and command.args.isdigit():
        if message.from_user.id == int(command.args):
            await message.answer(
                TextFormatter(
                    "error:join_yourself",
                    message.from_user.language_code
                ).text
            )
        # TODO этот юзер - reffered
        return

    await menu.send_menu_message(message)


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

    await menu.send_menu_message(message)
