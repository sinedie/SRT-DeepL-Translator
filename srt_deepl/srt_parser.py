import srt
import logging


def open_srt(file_path):
    logging.info(f"Reading {file_path}")

    with open(file_path, "r", errors="ignore") as srt_file:
        srt_file = srt.parse(srt_file)
        subs = list(srt_file)
        subs = list(srt.sort_and_reindex(subs))

        for sub in subs:
            sub.content = srt.make_legal_content(sub.content)
            sub.content = sub.content.strip().replace("\n", " ")

        return subs


def get_srt_portions(subtitles, characters=4500):
    portion = []

    for subtitle in subtitles:
        n_char = sum(len(sub.content) for sub in portion) + len(subtitle.content)

        if n_char >= characters and len(portion) != 0:
            yield portion
            portion = []

        portion.append(subtitle)

    yield portion


def wrap_line(text, max_char):
    wraped_lines = []
    for word in text.split():
        if len(wraped_lines) != 0 and len(wraped_lines[-1]) + len(word) < max_char:
            wraped_lines[-1] += f" {word}"
        else:
            wraped_lines.append(f"{word}")

    return '\n'.join(wraped_lines)


def save_srt(file_name, lang_to, subs):

    logging.info(f"Saving {file_name}_{lang_to}")
    subs = srt.compose(subs)
    with open(f"{file_name}_{lang_to}.srt", "w") as file_out:
        file_out.write(subs)
