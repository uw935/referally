from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ...texts import TextFormatter
from ...states import ReffedUserState
from ...keyboard import SubscribeKeyboard


router = Router()
router.message.filter(ReffedUserState.MENU)


async def send_channel_link(
    message: Message,
    state: FSMContext | None = None,
    lang_code: str | None = None
) -> None:
    """
    Send link to channel for Refered Users

    :param message: Telegram message
    :param state: User's state. Optional
    :param lang_code: User's language code. Optional
    """

    if state is not None:
        await state.set_state(ReffedUserState.MENU)

    lang_code = lang_code or message.from_user.language_code

    await message.answer(
        TextFormatter("refd_user:channel", lang_code).text,
        reply_markup=SubscribeKeyboard(lang_code).markup
    )


@router.message()
async def reffed_user_message_handler(message: Message) -> None:
    """
    All the messages handler for reffed user

    :param message: Message
    """

    await send_channel_link(message)
