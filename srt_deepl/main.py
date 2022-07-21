import os
import glob
import logging

from fp.fp import FreeProxy
from get_gecko_driver import GetGeckoDriver
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from typing import List

from .deepl import DeeplTranslator
from .srt_parser import SrtFile


# Check if the current version of geckodriver exists
get_driver = GetGeckoDriver()
get_driver.install()


def create_proxy() -> Proxy:
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
    wrap_limit: int = 50,
) -> None:

    if driver is None:
        proxy = create_proxy()
        driver = create_driver(proxy)

    translator = DeeplTranslator(driver, lang_from, lang_to)

    for fpath in get_srt_files(folder):
        srt = SrtFile(fpath)
        srt.translate(translator)
        srt.wrap_lines(wrap_limit)
        srt.save(f"{os.path.splitext(fpath)[0]}_{lang_to}.srt")

    logging.info("Closing browser")
    driver.close()
