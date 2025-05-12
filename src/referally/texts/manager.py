import re
from loguru import logger

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
        skip_md_check: bool = False,
        **kwargs
    ) -> None:
        """
        Initialization of TextFormatter

        :param path: Path of the text from JSON's
        example: ["text"]["subtext"] = "text:subtext"
        :param skip_md_check: True if it should skip the Markdown
        check for args in kwargs
        :param kwargs: Arguments that required in the text
        """

        locale_text = LocaleManager.get_text(lang_code)

        for name in path.split(":"):
            locale_text = locale_text.get(name)

            if locale_text is None:
                locale_text = "Sorry, but this text couldn't be displayed"
                logger.error(f"Path \"{path}\" not found")
                break

        self.text = locale_text

        for element in kwargs:
            kwargs[element] = str(kwargs[element])

            if skip_md_check is False:
                kwargs[element] = re.sub(
                    r"([_*\[\]()~`>#+\-=|{}.!])",
                    r"\\\1",
                    kwargs[element]
                )

            self.text = self.text.replace(
                "{" f"{element}" "}",
                kwargs[element]
            )
