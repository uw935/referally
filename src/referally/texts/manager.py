import re
from loguru import logger

from ..config import Config
from .locales import LocaleManager


class TextFormatter:
    """
    Control every aspect of text display

    Formatting, Markdowning & replacing args
    """

    text: str

    def __init__(
        self,
        path: str,
        lang_code: str = Config.DEFAULT_LANG,
        skip_md_check: bool = False,
        **kwargs
    ) -> None:
        """
        Initialization of TextFormatter

        :param path: Path of the text from JSON's. See `more about` it below
        :param lang_code: Text's langauge code that is needed
        :param skip_md_check: True if skip the Markdown check
        for args in kwargs
        :param kwargs: Arguments that required in the text

        ## More about `path`
        It's the path to the text from .JSON, all names separated by ":"

        Example
            1. **keyboard:list:back** — references to back button text
            in list in keyboard
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
