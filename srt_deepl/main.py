import os
import glob
import logging
import geckodriver_autoinstaller

from .deepl import Translator
from .srt_parser import wrap_line, save_srt

# Check if the current version of geckodriver exists
geckodriver_autoinstaller.install()

INPUT_LANG = {
    "auto": "Any language (detect)",
    "bg": "Bulgarian",
    "zh": "Chinese",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
}

OUTPUT_LANG = {
    "bg": "Bulgarian",
    "zh": "Chinese (simplified)",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "pl": "Polish",
    "pt": "Portuguese",
    "br": "Portuguese (Brazilian)",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
}


def translate(filepath, lang_from, lang_to, wrap_limit, delete_old):
    translator = Translator()

    lang_from = {
        "lang": lang_from,
        "description": INPUT_LANG[lang_from],
    }
    lang_to = {
        "lang": lang_to,
        "description": OUTPUT_LANG[lang_to],
    }

    if type(filepath) == str:
        filepath = [filepath]
    elif type(filepath) != list:
        raise TypeError("Filepath must be str or list")

    files = []
    for fpath in filepath:
        if os.path.isdir(fpath):
            files += glob.glob(fpath + "/**/*.srt", recursive=True)
        elif os.path.splitext(fpath)[-1].lower() == ".srt":
            files.append(fpath)

    for fpath in files:
        subs = translator.translate(
            fpath,
            lang_from,
            lang_to,
            wrap_limit,
        )

        for sub in subs:
            if len(sub.content) > wrap_limit:
                sub.content = wrap_line(sub.content, wrap_limit)

        fname = os.path.splitext(fpath)[0]
        save_srt(fname, lang_to["lang"], subs)

    translator.close()