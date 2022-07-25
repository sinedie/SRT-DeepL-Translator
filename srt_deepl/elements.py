import sys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


class BaseElement:
    def __init__(
        self,
        driver: webdriver,
        locate_by: str,
        locate_value: str,
        multiple: bool = False,
        wait_time: int = 100,
    ) -> None:

        self.driver = driver
        locator = (getattr(By, locate_by.upper(), "id"), locate_value)
        find_element = driver.find_elements if multiple else driver.find_element
        try:
            WebDriverWait(driver, wait_time).until(
                lambda driver: find_element(*locator)
            )
            self.element = find_element(*locator)
        except TimeoutException:
            print(f"Timed out trying to get element ({locate_by} = {locate_value})")
            logging.info("Closing browser")
            driver.close()
            sys.exit()


class Text(BaseElement):
    @property
    def text(self) -> str:
        return self.element.get_attribute("text")


class TextArea(BaseElement):
    def write(self, value: str) -> None:
        self.element.clear()
        self.element.send_keys(*value)

    @property
    def value(self) -> None:
        return self.element.get_attribute("value")


class Button(BaseElement):
    def click(self) -> None:
        try:
            can_click = getattr(self.element, "click", None)
            if callable(can_click):
                self.element.click()
        except:
            # Using javascript if usual click function does not work
            self.driver.execute_script("arguments[0].click();", self.element)
