import argparse
import easygui
import logging

from .main import INPUT_LANG, OUTPUT_LANG, translate

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
    ).split("-")[0].strip()
    args.output_lang = easygui.choicebox(
        choices=[
            f"{lang} - [{description}]" for lang, description in OUTPUT_LANG.items()
        ]
    ).split("-")[0].strip()

if not args.show_browser:
    os.environ["MOZ_HEADLESS"] = "1"

translate(
    args.filepath,
    args.input_lang,
    args.output_lang,
    args.wrap_limit,
    args.delete,
)

