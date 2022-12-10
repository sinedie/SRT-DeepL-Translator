import logging
import time

from translatepy import Translate

from .srt_parser import open_srt, get_srt_portions


class Translator:
    def __init__(self):
        self.translator = Translate()

    def translate(self, file_path, lang_from, lang_to, wrap_limit):
        subs = open_srt(file_path)

        for portion in get_srt_portions(subs):
            text = [sub.content for sub in portion]
            text = "\n".join(text)

            logging.info("Copying portion of file")
            logging.info("Waiting for translation to complete")
            for _ in range(60):  # Maximun number of iterations 60 seconds
                translation = self.translator.translate(text, lang_to['lang'], lang_from['lang']).result
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
