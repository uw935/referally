"""
Text formatter manager
"""

import re

from ..config import Config
from .locales import LocaleManager


class TextFormatter:
    """
    Control every aspect of text display

    Formatting, Markdowning & replacing args
    """

    text: str = None

    def __init__(
        self,
        path: str,
        lang_code: str = Config.DEFAULT_LANG,
        /,
        **kwargs
    ) -> None:
        """
        Initialization of Text

        :param path: Path of the text from JSON's
        example: ["text"]["subtext"] = "text:subtext"
        :param kwargs: Arguments that required in the text
        """

        self.text = LocaleManager.get_text(lang_code)

        for name in path.split(":"):
            self.text = self.text[name]

        for element in kwargs:
            kwargs[element] = re.sub(
                r"([_*\[\]()~`>#+\-=|{}.!])",
                r"\\\1",
                str(kwargs[element])
            )

            self.text = self.text.replace(
                "{" f"{element}" "}",
                kwargs[element]
            )
