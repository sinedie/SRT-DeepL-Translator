from selenium import webdriver
from .elements import Text


def get_proxies(https=True):
    driver = webdriver.Firefox()
    driver.get("https://free-proxy-list.net/")

    proxies = []
    table_rows = Text(driver, "XPATH", "//tr[@role='row']", multiple=True).text
    for proxy in table_rows:
        proxy = proxy.split()
        proxy = {"ip": proxy[0], "port": proxy[1], "https": "yes" in proxy}
        if not https or proxy["https"]:
            proxies.append(f"{proxy['ip']}:{proxy['port']}")

    driver.close()

    return proxies
