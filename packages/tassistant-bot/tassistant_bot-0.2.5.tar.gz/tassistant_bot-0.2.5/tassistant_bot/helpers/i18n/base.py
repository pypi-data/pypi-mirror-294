import os
import json
import re
from typing import Dict, Optional
from logging import getLogger

from tassistant_bot.helpers import SingletonMeta

logger = getLogger()


def process_json_file(file_path: str) -> Dict:
    """
    Processes a JSON file and returns its data as a dictionary.

    :param file_path: Path to the JSON file.
    :return: Data from the JSON file as a dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def process_txt_file(file_path: str) -> str:
    """
    Processes a text file and returns its content as a string.

    :param file_path: Path to the text file.
    :return: Content of the text file as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_locales(locale_dir: str) -> Dict[str, Dict[str, str]]:
    """
    Loads locales from the specified directory.

    Walks through all files in the directory and subdirectories. JSON files
    are processed as dictionaries, and text files are processed as strings.

    :param locale_dir: Path to the directory containing locale files.
    :return: A dictionary where keys are directory names (name of language) and values are dictionaries of locales.
    """
    locales = {}
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            dir_name = re.findall(r"[^\\/]+", root)[-1]
            file_path = os.path.join(root, file)

            if dir_name not in locales:
                locales[dir_name] = {}

            if file.endswith(".json"):
                locales[dir_name].update(process_json_file(file_path))
            elif file.endswith(".txt"):
                file_name = file.replace(".txt", "").upper()
                locales[dir_name][file_name] = process_txt_file(file_path)

    return locales


class I18n(metaclass=SingletonMeta):
    """
    A class for handling internationalization (i18n) with support for multiple locales.

    Uses Singleton pattern
    """

    def __init__(self, locale: str = "ru", locale_dir: str = "locale") -> None:
        """
        :param locale: The locale to use. If None, defaults to "ru".
        :param locale_dir: The directory containing locale files. Defaults to "locale".
        """
        self._current_locale = locale
        self._locale_dir = os.path.join(os.getcwd(), locale_dir)
        self._locales: Dict[str, Dict[str, str]] = {}

        self.get_locales()

    def update_locales(
        self, locales: Dict[str, Dict[str, str]], module: Optional[str] = None
    ) -> None:
        """
        Updates the private variable locales with new data.
        Data updating not rewriting

        :param locales: A dictionary of locales to update.
        :param module: Optional module name to organize the locales. If provided,
                       locales will be updated under this module.
        """
        for locale, translations in locales.items():
            if locale not in self._locales:
                self._locales[locale] = {}

            if module:
                self._locales[locale][module] = translations
            else:
                self._locales[locale].update(translations)

    def get_locales(self) -> None:
        """
        Loads locales from the directory specified during initialization and updates
        the internal locale data.

        Uses for scan locale dir of a user bot, not a modules

        :return: None
        """
        locales = get_locales(self._locale_dir)
        self.update_locales(locales)

    def create_module_get(self, module_name: str):
        def new_get_function(query, data: Optional[Dict[str, str]] = None):
            search_query = f"{module_name}:{query}"
            return self.get(search_query, data)

        return new_get_function

    def get(self, name: str, data: Optional[Dict[str, str]] = None) -> str:
        """
        Retrieves a localized string for the given name and optionally replaces placeholders
        with the provided data.

        :param name: The name of the localized string, which should be in uppercase.
        :param data: An optional dictionary of placeholder values to replace in the string.
        :return: The formatted localized string, or the name if not found.
        """
        is_module = ":" in name
        module: Optional[str] = None

        if is_module:
            parts = name.split(":")
            module = parts[0]
            name = parts[1]
            if not name.isupper():
                logger.warning(
                    f"| Localization | use upper key name, provided value: {name}"
                )

        name = name.upper()

        try:
            raw_message = (
                self._locales[self._current_locale][module][name]
                if is_module
                else self._locales[self._current_locale][name]
            )

            if data:
                message = raw_message
                for key, value in data.items():
                    message = message.replace(f"%{key}%", str(value))
                return message

            return raw_message

        except KeyError:
            logger.error(
                f"| Localization | provided key does not exist | {self._current_locale} | {name}"
            )
            return name
