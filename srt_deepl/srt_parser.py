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

        if n_char >= characters:
            yield portion
            portion = []

        portion.append(subtitle)

    yield portion


def wrap_line(text, max_char):
    new_text = ""
    for word in text.split():
        n_lines = max_char * (len(new_text) // max_char)
        if len(new_text) - n_lines + len(word) < max_char:
            new_text += f"{word} "
        else:
            new_text += f"\n{word} "

    return new_text


def save_srt(file_name, lang_to, subs):

    logging.info(f"Saving {file_name}_{lang_to}")
    subs = srt.compose(subs)
    with open(f"{file_name}_{lang_to}.srt", "w") as file_out:
        file_out.write(subs)
