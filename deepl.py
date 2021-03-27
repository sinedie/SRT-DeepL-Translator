import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from srt import SRT


class translator:
    def __init__(self):

        ### Opening browser
        logging.info("Opening browser")
        geckodriver_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "geckodriver")
        )
        self.browser = webdriver.Firefox(executable_path=geckodriver_path)
        self.browser.maximize_window()

        ### Going to deepl.com
        logging.info("Going to deepl.com")
        self.browser.get("https://www.deepl.com/translator")

        ### Getting source and target inputs
        logging.info("Getting source and target inputs")
        self.inputElement = self.browser.find_element_by_class_name(
            "lmt__source_textarea"
        )
        self.targetElement = self.browser.find_element_by_class_name(
            "lmt__target_textarea"
        )

        # Need to hide the cookiebanner so that way it doesnt obscure the language options
        # Maybe there's a better way, but this works for now. Feel free to change it
        cookieBanner = self.browser.find_element_by_id("dl_cookieBanner")
        self.browser.execute_script(
            "arguments[0].style.visibility='hidden'", cookieBanner
        )

    def is_translated(self, text, traslation):

        return (
            len(traslation) != 0
            and len(text.splitlines()) == len(traslation.splitlines())
            and "[...]" not in traslation
        )

    def choose_language(self, languageSelect, lang):
        def is_the_right_language(button, language):
            button_dl_test_attrivute = button.get_attribute("dl-test").lower()
            return button_dl_test_attrivute.endswith(language)

        languageSelect.click()

        languages_menu = languageSelect.find_element_by_class_name(
            "lmt__language_select__menu"
        )
        languagesButtons = languages_menu.find_elements_by_tag_name("button")
        languageButton = next(
            (
                button
                for button in languagesButtons
                if is_the_right_language(button, lang)
            ),
            None,
        )

        if not languageButton:
            print(
                f"ERROR: Language {lang} was not found. Maybe you choose the same on both?"
            )
            self.close()
            os._exit(os.EX_OK)
            return

        languageButton.click()

    def translate_srt(self, file_path, lang_from, lang_to, wrap_line_limit, delete_old):

        logging.info(f"Traslating file {file_path}")
        srt_file = SRT(file_path)

        sub_id = 0  # ID of initial subtitle
        while sub_id < srt_file.n_subtitles:

            # Clearing input
            logging.info("Clearing input")
            self.inputElement.clear()

            while len(self.targetElement.get_attribute("value")) != 0:
                time.sleep(1)

            # Portion to of srt to translate
            logging.info("Getting portion of srt to translate")
            text, sub_id_f = srt_file.extract_portion(sub_id)

            # Sending text
            logging.info("Writing portion on input")
            self.inputElement.send_keys(text)

            # Getting traslation
            logging.info("Traslating portion")
            while not self.is_translated(
                text, self.targetElement.get_attribute("value")
            ):
                time.sleep(1)

            traslation = self.targetElement.get_attribute("value").splitlines()

            # Updating text on SRT
            logging.info("Saving portion")
            srt_file.update_text(sub_id, traslation)

            # Getting next portion
            sub_id = sub_id_f

        # Wraping lines
        logging.info(f"Wraping lines")
        srt_file.wrap_lines(wrap_line_limit)

        # Saving file
        filename = os.path.splitext(file_path)[0]
        file_out = f"{filename}_{lang_to}.srt"

        logging.info(f"Saving {file_out}")
        srt_file.save(file_out)

        if delete_old:
            logging.info(f"Deleting file {file_path}")
            os.remove(file_path)

    def traslate_all(self, file_paths, lang_from, lang_to, wrap_line_limit, delete_old):
        for path in file_paths:

            if not os.path.exists(path):
                print(f"INFO: File {path} doesn't exist, skipping...")
                continue

            if os.path.isdir(path):
                files_in_dir = os.listdir(path)

                for file_name in files_in_dir:
                    file_path = os.path.join(path, file_name)
                    self.traslate_all(
                        [file_path], lang_from, lang_to, wrap_line_limit, delete_old
                    )

                return

            extension = os.path.splitext(path)[1]
            if extension.lower() == ".srt":
                self.translate_srt(
                    path, lang_from, lang_to, wrap_line_limit, delete_old
                )

    def translate(
        self,
        file_paths,
        lang_from,
        lang_to,
        wrap_line_limit=20,
        delete_old=False,
    ):

        ### Preparing page
        languageToSelect = self.browser.find_element_by_class_name(
            "lmt__language_select--target"
        )
        languageFromSelect = self.browser.find_element_by_class_name(
            "lmt__language_select--source"
        )

        self.choose_language(languageFromSelect, lang_from)
        self.choose_language(languageToSelect, lang_to)

        self.traslate_all(file_paths, lang_from, lang_to, wrap_line_limit, delete_old)

    def close(self):
        self.browser.quit()