"""
Localization Manager

This buddy knows every language from base localizations folder
"""

from ...config import Config
from .parser import LocaleFileParser


TEXTS: dict = LocaleFileParser.parse()


class LocaleManager:
    """
    Localization manager
    """

    @staticmethod
    def get_text(lang_code: str = Config.DEFAULT_LANG) -> str:
        """
        Get text by lang_code

        :param lang_code: Telegram language code
        :return: Text from lang_code locale
        """

        return TEXTS.get(lang_code) or TEXTS[Config.DEFAULT_LANG]
