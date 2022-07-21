import re
import srt
import logging

from typing import List, Any, Generator

from .deepl import Translator


class SrtFile:
    subtitles = []
    portion_sizes = 4500

    def __init__(self, file_path: str) -> None:
        logging.info(f"Reading {file_path}")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as input_file:
            srt_file = srt.parse(input_file)
            subtitles = list(srt_file)
            subtitles = list(srt.sort_and_reindex(subtitles))
            self.subtitles = self.clean_subs_content(subtitles)

    def __iter__(self) -> Generator:
        portion = []

        for subtitle in self.subtitles:
            n_char = sum(len(sub.content) for sub in portion) + len(subtitle.content)

            if n_char >= self.portion_sizes and len(portion) != 0:
                yield portion
                portion = []

            portion.append(subtitle)

        yield portion

    def clean_subs_content(self, subtitles: List[Any]) -> List[Any]:
        cleanr = re.compile("<.*?>")

        for sub in subtitles:
            sub.content = cleanr.sub("", sub.content)
            sub.content = srt.make_legal_content(sub.content)
            sub.content = sub.content.strip().replace("\n", " ")

        return subtitles

    def wrap_lines(self, wrap_limit: int) -> None:
        for sub in self.subtitles:
            if len(sub.content) > wrap_limit:
                sub.content = self.wrap_line(sub.content, wrap_limit)

    def wrap_line(self, text: str, max_char: int) -> str:
        wraped_lines = []
        for word in text.split():
            if len(wraped_lines) != 0 and len(wraped_lines[-1]) + len(word) < max_char:
                wraped_lines[-1] += f" {word}"
                continue

            wraped_lines.append(f"{word}")

        return "\n".join(wraped_lines)

    def translate(self, translator: Translator) -> None:
        for subs_slice in self:
            text = [sub.content for sub in subs_slice]
            text = "\n".join(text)

            translation = translator.translate(text)
            translation = translation.splitlines()

            logging.info("Updating portion with translation")
            for i in range(len(subs_slice)):
                subs_slice[i].content = translation[i]

    def save(self, filepath: str) -> None:
        logging.info(f"Saving {filepath}")
        subtitles = srt.compose(self.subtitles)
        with open(filepath, "w", encoding="utf-8") as file_out:
            file_out.write(subtitles)
