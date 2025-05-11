"""
This guy parses all the languages from localizations folder

Only for locales module
"""

import os
import json
from loguru import logger


LOCALIZATIONS_BASE_FOLDER: str = "../localizations/"


class LocaleFileParser:
    """
    Parsing localizations
    """

    @staticmethod
    def parse() -> dict:
        """
        Parse localizations from base folder

        Maybe in the future this guy
        will also check structure of the file
        """

        result = {}

        logger.info("Start languages parsing", source=__name__)

        for filename in os.listdir(LOCALIZATIONS_BASE_FOLDER):
            if filename[-5:] != ".json":
                continue

            with open(
                f"{LOCALIZATIONS_BASE_FOLDER}{filename}",
                "r",
                encoding="UTF-8"
            ) as jsonfile:
                lang_code = filename[:-5]
                logger.info(f"Parsing {lang_code}", source=__name__)

                result[lang_code] = json.load(jsonfile)

        logger.info(
            f"Parsed {len(result.keys())} languages",
            source=__name__
        )

        return result
