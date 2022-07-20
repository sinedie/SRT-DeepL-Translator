import logging
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from .elements import TextArea, Button
from .srt_parser import open_srt, get_srt_portions


class Translator:
    def __init__(self, driver):
        self.driver = driver

        logging.info("Going to DeepL")
        self.driver.get("https://www.deepl.com/translator")

        self.actions = ActionChains(self.driver)
        self.input_lang_from = TextArea(
            self.driver,
            "CLASS_NAME",
            "lmt__source_textarea",
        )
        self.input_lang_to = TextArea(
            self.driver,
            "CLASS_NAME",
            "lmt__target_textarea",
        )

    def close(self):
        logging.info("Closing browser")
        self.driver.close()

    def choose_languages(self, lang_from, lang_to):
        Button(
            self.driver,
            "CLASS_NAME",
            "lmt__language_select--source",
        ).click()

        Button(
            self.driver,
            "XPATH",
            f"//button[@dl-test='translator-lang-option-{lang_from['lang'].lower()}'] | //button[text()='{lang_from['description']}']",
        ).click()

        Button(
            self.driver,
            "CLASS_NAME",
            "lmt__language_select--target",
        ).click()

        Button(
            self.driver,
            "XPATH",
            f"//button[@dl-test='translator-lang-option-{lang_to['lang'].lower()}'] | //button[text()='{lang_to['description']}']",
        ).click()

    def translate(self, file_path, lang_from, lang_to, wrap_limit):

        self.choose_languages(lang_from, lang_to)

        subs = open_srt(file_path)

        for portion in get_srt_portions(subs):
            text = [sub.content for sub in portion]
            text = "\n".join(text)

            logging.info("Copying portion of file")
            self.input_lang_from.write((text))

            logging.info("Waiting for translation to complete")
            for _ in range(60):  # Maximun number of iterations 60 seconds
                translation = self.input_lang_to.value
                if (
                    len(translation) != 0
                    and len(text.splitlines()) == len(translation.splitlines())
                    and "[...]" not in translation
                ):
                    break
                time.sleep(1)

            else:
                raise Exception(
                    """Timeout for traslating portion.\n
                    Make sure your SRT file does not contain the characters '[...]'"""
                )

            if text == translation:
                raise Exception(
                    """No translation occurred.\n
                    Make sure your SRT file does not contain HTML tags and/or HTML elements'"""
                )

            logging.info("Updating portion with translation")
            translation = translation.splitlines()

            for i in range(len(portion)):
                portion[i].content = translation[i]

        return subs
