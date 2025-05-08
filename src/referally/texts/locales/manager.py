"""
Localization Manager

This buddy knows every language from base localizations folder
"""

from ...config import Config
from .parser import LocaleFileParser


_TEXTS: dict = LocaleFileParser.parse()


class LocaleManager:
    """
    Localization manager
    """

    @staticmethod
    def get_text(lang_code: str = Config.DEFAULT_LANG) -> dict:
        """
        Get texts by lang_code

        :param lang_code: Telegram language code
        :return: Texts of lang_code in dict
        """

        return _TEXTS.get(lang_code) or _TEXTS[Config.DEFAULT_LANG]
