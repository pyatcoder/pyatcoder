import re
from typing import Pattern


class LanguageNotFoundError(Exception):
    pass


class CodeStyle:
    def __init__(self,
                 indent_width=None
                 ):
        self.indent_width = indent_width


class Language:
    def __init__(self,
                 name: str,
                 display_name: str,
                 extension: str,
                 submission_lang_pattern: Pattern[str],
                 ):
        self.name = name
        self.display_name = display_name
        self.extension = extension
        self.submission_lang_pattern = submission_lang_pattern

    def source_code_name(self, name_without_extension: str) -> str:
        # put extension to the name
        return "{}.{}".format(name_without_extension, self.extension)

    @classmethod
    def from_name(cls, name: str):
        for lang in ALL_LANGUAGES:
            if lang.name == name:
                return lang
        raise LanguageNotFoundError(
            "No language support for '{}'".format(ALL_LANGUAGE_NAMES))


PYTHON = Language(
    name="python",
    display_name="Python",
    extension="py",
    submission_lang_pattern=re.compile(".*Python.*|^Python$"),
)

ALL_LANGUAGES = [PYTHON]
ALL_LANGUAGE_NAMES = [lang.display_name for lang in ALL_LANGUAGES]
