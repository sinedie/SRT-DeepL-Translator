import os
import glob
import logging
import deepl
import geckodriver_autoinstaller

from srt_parser import wrap_line, save_srt

# Check if the current version of geckodriver exists
geckodriver_autoinstaller.install()

INPUT_LANG = {
    "auto": "Any language (detect)",
    "bg": "Bulgarian",
    "zh": "Chinese",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
}

OUTPUT_LANG = {
    "bg": "Bulgarian",
    "zh": "Chinese (simplified)",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "pl": "Polish",
    "pt": "Portuguese",
    "br": "Portuguese (Brazilian)",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
}


def translate(filepath, lang_from, lang_to, wrap_limit, delete_old):
    translator = deepl.Translator()

    lang_from = {
        "lang": lang_from,
        "description": INPUT_LANG[lang_from],
    }
    lang_to = {
        "lang": lang_to,
        "description": OUTPUT_LANG[lang_to],
    }

    if type(filepath) == str:
        filepath = [filepath]
    elif type(filepath) != list:
        raise TypeError("Filepath must be str or list")

    files = []
    for fpath in filepath:
        if os.path.isdir(fpath):
            files += glob.glob(fpath + "/**/*.srt", recursive=True)
        elif os.path.splitext(fpath)[-1].lower() == ".srt":
            files.append(fpath)

    for fpath in files:
        subs = translator.translate(
            fpath,
            lang_from,
            lang_to,
            wrap_limit,
        )

        for sub in subs:
            if len(sub.content) > wrap_limit:
                sub.content = wrap_line(sub.content, wrap_limit)

        fname = os.path.splitext(fpath)[0]
        save_srt(fname, lang_to["lang"], subs)

    translator.close()


if __name__ == "__main__":
    import argparse
    import easygui

    parser = argparse.ArgumentParser(
        description="Translates .STR files using DeepL.com",
    )

    parser.add_argument(
        "filepath",
        metavar="path",
        type=str,
        nargs="?",
        help="Files to convert (if directory traslates all srt files recursively)",
    )

    parser.add_argument(
        "-i",
        "--input-lang",
        type=str,
        default="auto",
        choices=INPUT_LANG.keys(),
        help="Language to translate from. Default: auto",
    )

    parser.add_argument(
        "-o",
        "--output-lang",
        type=str,
        default="es",
        choices=OUTPUT_LANG.keys(),
        help="Language to translate to. Default: es (spanish)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
        help="Increase output verbosity",
    )

    parser.add_argument(
        "-vv",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
        help="Increase output verbosity for debugging",
    )

    parser.add_argument(
        "-g",
        "--show-gui",
        action="store_true",
        help="Show configuration graphical interface",
    )

    parser.add_argument(
        "-s",
        "--show-browser",
        action="store_true",
        help="Show browser window",
    )

    parser.add_argument(
        "-w",
        "--wrap-limit",
        type=int,
        default=50,
        help="Number of characters to wrap the line. Including spaces. Default: 50",
    )

    parser.add_argument(
        "-x", "--delete", action="store_true", help="Delete files when traslated"
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    if not args.filepath:
        args.filepath = easygui.diropenbox(title="Choose the folder where the .SRT are")

    if not args.filepath:
        raise Exception("No folder found")

    if args.show_gui:
        args.input_lang = easygui.choicebox(
            choices=[
                f"{lang} - [{description}]" for lang, description in INPUT_LANG.items()
            ]
        ).split("-")[0]
        args.output_lang = easygui.choicebox(
            choices=[
                f"{lang} - [{description}]" for lang, description in OUTPUT_LANG.items()
            ]
        ).split("-")[0]

    if not args.show_browser:
        os.environ["MOZ_HEADLESS"] = "1"

    translate(
        args.filepath,
        args.input_lang,
        args.output_lang,
        args.wrap_limit,
        args.delete,
    )

else:
    os.environ["MOZ_HEADLESS"] = "1"