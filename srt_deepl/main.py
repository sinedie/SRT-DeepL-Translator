import os
import glob
import logging
import random
import geckodriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType

from .deepl import Translator
from .srt_parser import wrap_line, save_srt
from .utils import get_proxies


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
    "id": "Indonesian",
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
    "tr": "Turkish",
    "uk": "Ukrainian",
}


OUTPUT_LANG = {
    "bg": "Bulgarian",
    "zh": "Chinese (simplified)",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en-US": "English (American)",
    "en-GB": "English (British)",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hu": "Hungarian",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "pl": "Polish",
    "pt-PT": "Portuguese",
    "pt-BR": "Portuguese (Brazilian)",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
    "tr": "Turkish",
    "uk": "Ukrainian",
}


def translate(
    filepath,
    lang_from,
    lang_to,
    wrap_limit=50,
    delete_old=False,
    driver=None,
):

    # Check if the current version of geckodriver exists
    geckodriver_autoinstaller.install()

    if driver is None:
        proxies = get_proxies()
        if len(proxies) == 0:
            proxies = get_proxies(https=False)

        my_proxy = random.choice(proxies)

        proxy = Proxy(
            {
                "proxyType": ProxyType.MANUAL,
                "httpProxy": my_proxy,
                "ftpProxy": my_proxy,
                "sslProxy": my_proxy,
                "noProxy": "",  # set this value as desired
            }
        )

        driver = webdriver.Firefox(proxy=proxy)
        driver.maximize_window()

    translator = Translator(driver)

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
