import os
import glob
import logging

from fp.fp import FreeProxy
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import WebDriverException
from typing import List

from .deepl import Translator, DeeplTranslator, GoogleTranslator
from .srt_parser import SrtFile


def create_proxy() -> Proxy:
    logging.info('Getting a new Proxy from https://www.sslproxies.org/')
    proxy = FreeProxy().get()
    proxy = Proxy(
        dict(
            proxyType=ProxyType.MANUAL,
            httpProxy=proxy,
            ftpProxy=proxy,
            sslProxy=proxy,
            noProxy="",
        )
    )
    return proxy


def create_driver(proxy: Proxy | None = None) -> WebDriver:
    logging.info('Creating Selenium Webdriver instance')
    try:
        driver = webdriver.Firefox(proxy=proxy)
    except WebDriverException:
        logging.info('Installing Firefox GeckoDriver cause it isn\'t installed')
        get_driver = GetGeckoDriver()
        get_driver.install()

        driver = webdriver.Firefox(proxy=proxy)

    driver.maximize_window()
    return driver


def get_srt_files(folder: str) -> List[str]:
    return glob.glob(os.path.join(folder, "**/*.srt"), recursive=True)


def translate(
    folder: str,
    lang_from: str,
    lang_to: str,
    driver: WebDriver | None = None,
    proxy: Proxy | None = None,
    wrap_limit: int = 50,
    translator: Translator = DeeplTranslator
) -> None:

    if proxy is None:
        proxy = create_proxy()

    if driver is None:
        driver = create_driver(proxy)

    translator_object = translator(driver, lang_from, lang_to)

    for fpath in get_srt_files(folder):
        srt = SrtFile(fpath)
        srt.translate(translator_object)
        srt.wrap_lines(wrap_limit)
        srt.save(f"{os.path.splitext(fpath)[0]}_{lang_to}.srt")

    logging.info("Closing browser")
    driver.close()
