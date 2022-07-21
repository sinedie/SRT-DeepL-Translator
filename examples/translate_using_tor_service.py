import logging

logging.basicConfig(level=logging.INFO)

from selenium import webdriver
from srt_deepl import translate

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9050)
profile.set_preference("network.proxy.socks_version", 5)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)

logging.info("Begin translate process")

translate(
    "C:\\srt", # folder where the .SRT files are
    "en", # original language
    "hu", # desired language
    wrap_limit=50,
    driver=driver,
)

logging.info("End of translate process")
