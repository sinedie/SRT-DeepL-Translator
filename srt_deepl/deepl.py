import time
import logging

from selenium.webdriver.remote.webdriver import WebDriver
from abc import ABC

from .elements import TextArea, Button, BaseElement, Text


class Translator(ABC):
    max_char: int

    def translate(self, text: str) -> str:
        pass


class DeeplTranslator(Translator):
    URL = "https://www.deepl.com/translator"
    max_char = 4500
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

        self.pop_up = BaseElement(driver, "CLASS_NAME", "lmt__progress_popup")
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

        # Get the language button to click based on is dl-test property or the text in the button
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
            and not self.pop_up.element.is_displayed()
        )

    def translate(self, text: str) -> str:
        self.input_lang_from.write((text))

        # Maximun number of iterations 60 seconds
        for _ in range(60):
            translation = self.input_lang_to.value
            if self.is_translated(text, translation):
                return translation
            time.sleep(1)

        raise Exception("Translation timed out")


class GoogleTranslator(Translator):
    URL = "https://translate.google.com/"
    max_char = 4500
    LANGUAGES = {
        "auto": "Detect language",
        "af": "Afrikaans",
        "sq": "Albanian",
        "am": "Amharic",
        "ar": "Arabic",
        "hy": "Armenian",
        "as": "Assamese",
        "ay": "Aymara",
        "az": "Azerbaijani",
        "bm": "Bambara",
        "eu": "Basque",
        "be": "Belarusian",
        "bn": "Bengali",
        "bho": "Bhojpuri",
        "bs": "Bosnian",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "ceb": "Cebuano",
        "ny": "Chichewa",
        "zh-CN": "Chinese",
        "co": "Corsican",
        "hr": "Croatian",
        "cs": "Czech",
        "da": "Danish",
        "dv": "Dhivehi",
        "doi": "Dogri",
        "nl": "Dutch",
        "en": "English",
        "eo": "Esperanto",
        "et": "Estonian",
        "ee": "Ewe",
        "tl": "Filipino",
        "fi": "Finnish",
        "fr": "French",
        "fy": "Frisian",
        "gl": "Galician",
        "ka": "Georgian",
        "de": "German",
        "el": "Greek",
        "gn": "Guarani",
        "gu": "Gujarati",
        "ht": "Haitian Creole",
        "ha": "Hausa",
        "haw": "Hawaiian",
        "iw": "Hebrew",
        "hi": "Hindi",
        "hmn": "Hmong",
        "hu": "Hungarian",
        "is": "Icelandic",
        "ig": "Igbo",
        "ilo": "Ilocano",
        "id": "Indonesian",
        "ga": "Irish",
        "it": "Italian",
        "ja": "Japanese",
        "jw": "Javanese",
        "kn": "Kannada",
        "kk": "Kazakh",
        "km": "Khmer",
        "rw": "Kinyarwanda",
        "gom": "Konkani",
        "ko": "Korean",
        "kri": "Krio",
        "ku": "Kurdish (Kurmanji)",
        "ckb": "Kurdish (Sorani)",
        "ky": "Kyrgyz",
        "lo": "Lao",
        "la": "Latin",
        "lv": "Latvian",
        "ln": "Lingala",
        "lt": "Lithuanian",
        "lg": "Luganda",
        "lb": "Luxembourgish",
        "mk": "Macedonian",
        "mai": "Maithili",
        "mg": "Malagasy",
        "ms": "Malay",
        "ml": "Malayalam",
        "mt": "Maltese",
        "mi": "Maori",
        "mr": "Marathi",
        "mni-Mtei": "Meiteilon (Manipuri)",
        "lus": "Mizo",
        "mn": "Mongolian",
        "my": "Myanmar (Burmese)",
        "ne": "Nepali",
        "no": "Norwegian",
        "or": "Odia (Oriya)",
        "om": "Oromo",
        "ps": "Pashto",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese",
        "pa": "Punjabi",
        "qu": "Quechua",
        "ro": "Romanian",
        "ru": "Russian",
        "sm": "Samoan",
        "sa": "Sanskrit",
        "gd": "Scots Gaelic",
        "nso": "Sepedi",
        "sr": "Serbian",
        "st": "Sesotho",
        "sn": "Shona",
        "sd": "Sindhi",
        "si": "Sinhala",
        "sk": "Slovak",
        "sl": "Slovenian",
        "so": "Somali",
        "es": "Spanish",
        "su": "Sundanese",
        "sw": "Swahili",
        "sv": "Swedish",
        "tg": "Tajik",
        "ta": "Tamil",
        "tt": "Tatar",
        "te": "Telugu",
        "th": "Thai",
        "ti": "Tigrinya",
        "ts": "Tsonga",
        "tr": "Turkish",
        "tk": "Turkmen",
        "ak": "Twi",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "ug": "Uyghur",
        "uz": "Uzbek",
        "vi": "Vietnamese",
        "cy": "Welsh",
        "xh": "Xhosa",
        "yi": "Yiddish",
        "yo": "Yoruba",
        "zu": "Zulu",
    }

    def __init__(self, driver: WebDriver, lang_in: str, lang_out: str) -> None:
        self.driver = driver
        self.open_webpage(driver)

        input_lang_from_xpath = "//textarea[@aria-label='Source text']"
        self.input_lang_from = TextArea(driver, "XPATH", input_lang_from_xpath)

        self.set_input_language(driver, lang_in)
        self.set_output_language(driver, lang_out)

    def open_webpage(self, driver: WebDriver) -> None:
        logging.info(f"Going to {self.URL}")
        driver.get(self.URL)

    def set_input_language(self, driver: WebDriver, lang: str) -> None:
        logging.info("Setting input language")
        self.set_language(driver, lang, "More source languages")

    def set_output_language(self, driver: WebDriver, lang: str) -> None:
        logging.info("Setting output language")
        self.set_language(driver, lang, "More target languages")

    def set_language(
        self, driver: WebDriver, lang: str, dropdown_area_label: str
    ) -> None:

        # Click the languages dropdown button
        xpath_aria = f"//button[@aria-label='{dropdown_area_label}']"
        Button(driver, "XPATH", xpath_aria).click()

        # Get the language button to click based on is dl-test property or the text in the button
        xpath_by_property = f"//div[@data-language-code='{lang}']"
        x_path_by_text = f"//div[text()='{self.LANGUAGES[lang]}']"

        xpath = f"{xpath_by_property} | {x_path_by_text}"

        # Click the wanted language button
        Button(driver, "XPATH", xpath).click()

    def is_translated(self, original: str, translation: str) -> bool:
        return (
            len(translation) != 0
            and len(original.splitlines()) == len(translation.splitlines())
            and original != translation
            and translation != "Translating..."
        )

    def translate(self, text: str) -> str:
        self.input_lang_from.write((text))

        input_lang_to_xpath = "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[8]/div/div[1]/span[1]/span/span"
        self.input_lang_to = Text(self.driver, "XPATH", input_lang_to_xpath)

        # Maximun number of iterations 60 seconds
        for _ in range(60):
            translation = self.input_lang_to.text
            if self.is_translated(text, translation):
                return translation
            time.sleep(1)

        raise Exception("Translation timed out")
