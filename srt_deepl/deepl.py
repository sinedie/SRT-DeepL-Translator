import time
import logging

from selenium.webdriver.remote.webdriver import WebDriver
from abc import ABC

from .elements import TextArea, Button


class Translator(ABC):
    def translate(self):
        pass


class DeeplTranslator(Translator):
    URL = "https://www.deepl.com/translator"
    LANGUAGES = dict(
        auto="Any language (detect)",
        bg="Bulgarian",
        zh="Chinese",
        cs="Czech",
        da="Danish",
        nl="Dutch",
        en="English",
        et="Estonian",
        fi="Finnish",
        fr="French",
        de="German",
        el="Greek",
        hu="Hungarian",
        it="Italian",
        ja="Japanese",
        lv="Latvian",
        lt="Lithuanian",
        pl="Polish",
        pt="Portuguese",
        ro="Romanian",
        ru="Russian",
        sk="Slovak",
        sl="Slovenian",
        es="Spanish",
        sv="Swedish",
    )

    def __init__(self, driver: WebDriver, lang_in: str, lang_out: str) -> None:
        self.open_webpage(driver)

        self.input_lang_from = TextArea(driver, "CLASS_NAME", "lmt__source_textarea")
        self.input_lang_to = TextArea(driver, "CLASS_NAME", "lmt__target_textarea")

        self.set_input_language(driver, lang_in)
        self.set_output_language(driver, lang_out)

    def open_webpage(self, driver: WebDriver) -> None:
        logging.info(f"Going to {self.URL}")
        driver.get(self.URL)

    def set_input_language(self, driver: WebDriver, lang: str) -> None:
        self.set_language(driver, lang, "lmt__language_select--source")

    def set_output_language(self, driver: WebDriver, lang: str) -> None:
        self.set_language(driver, lang, "lmt__language_select--target")

    def set_language(self, driver: WebDriver, lang: str, dropdown_class: str) -> None:
        # Click the languages dropdown button
        Button(driver, "CLASS_NAME", dropdown_class).click()

        # Get the language button to click based on is dl-test property or the
        # text in the button
        xpath_by_property = f"//button[@dl-test='translator-lang-option-{lang}']"
        x_path_by_text = f"//button[text()='{self.LANGUAGES[lang]}']"
        xpath = f"{xpath_by_property} | {x_path_by_text}"

        # Click the wanted language button
        Button(driver, "XPATH", xpath).click()

    def is_translated(self, original: str, translation: str) -> bool:
        return (
            len(translation) != 0
            and "[...]" not in translation
            and len(original.splitlines()) == len(translation.splitlines())
            and original != translation
        )

    def translate(self, text: str) -> str:
        self.input_lang_from.write((text))

        # Maximun number of iterations 60 seconds
        for _ in range(60):
            translation = self.input_lang_to.value
            if self.is_translated(text, translation):
                return translation
            time.sleep(1)

        raise Exception("""Translation timed out""")
