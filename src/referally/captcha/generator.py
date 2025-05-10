"""
Disclaimer

At this moment, Captcha is actually easy to bypass:
just remember all of the choices here and check them.

However there is another goal for this. Read more in /docs/product.md
"""

import time
import random

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup
)

from ..keyboard import (
    create_button,
    create_markup
)


CAPTCHA_MAX_OBJECTS: int = 4
CAPTCHA_OBJECTS: dict = {
    "pig": "🐖",
    "policeman": "👮‍♀️",
    "programmer": "👨‍💻",
    "santa": "🎅",
    "penguin": "🐧"
}


class GeneratedCaptcha:
    """
    Datatype for generated captcha
    """

    id: int
    text: str
    keyboard: InlineKeyboardMarkup


class Captcha:
    """
    Class represent Captcha generation    
    """

    def __init__(self, callback: CallbackQuery) -> None:
        """
        Initializae Captcha class

        :param callback: Callback of Captcha buttons

        ## About callback
        It must some have space at the end.
        It will receive following data starting with "_":

        1. ID of Captcha
        2. Current button name (to verify it)

        ### Example
        CAPTCHA_RESOLVE_2424234_policeman

        Where 2424234 is Captcha ID and policeman is button name
        """

        self.callback = callback

    def generate(self) -> GeneratedCaptcha:
        """
        Generate Captcha

        :return: ID, text for display and verify and inline keyboard
        """

        result = GeneratedCaptcha
        result.id = int(time.time())
        captcha_objects_keys = list(CAPTCHA_OBJECTS.keys())

        result.text = random.choice(captcha_objects_keys)
        captcha_objects_keys.remove(result.text)

        random_button_index = random.randint(0, CAPTCHA_MAX_OBJECTS - 1)
        buttons = []

        for button_index in range(0, CAPTCHA_MAX_OBJECTS):
            element = result.text

            # This made for replacing "verify" button in random position
            # in the random position
            if button_index != random_button_index:
                element = random.choice(captcha_objects_keys)
                captcha_objects_keys.remove(element)

            buttons.append(
                create_button(
                    f"{CAPTCHA_OBJECTS[element]}",
                    f"{self.callback}_{result.id}_{element}"
                )
            )

        result.keyboard = create_markup(buttons)

        return result
