import os
import argparse
import logging

import deepl


parser = argparse.ArgumentParser(
    description='Translates .STR files using DeepL.com'
)

parser.add_argument(
    'filepath',
    metavar='path',
    type=str,
    nargs='+',
    help='Files to convert (if directory traslates all srt files recursively)'
)

parser.add_argument(
    '-i',
    '--input-lang',
    type=str,
    default='auto',
    choices=('auto', 'chinese', 'dutch', 'english', 'french', 'german',
            'italian', 'japanese', 'polish', 'portuguese', 'russian', 'spanish'),
    help='Language to translate from'
)

parser.add_argument(
    '-o',
    '--output-lang',
    type=str,
    default='spanish',
    choices=('chinese', 'dutch', 'english-us', 'english-uk', 'french', 'german',
            'italian', 'japanese', 'polish', 'portuguese', 'portuguese-br', 'russian', 'spanish'),
    help='Language to translate to'
)

parser.add_argument(
    '-v',
    '--verbose',
    action="store_const",
    dest="loglevel",
    const=logging.INFO,
    help="Increase output verbosity",
)

parser.add_argument(
    '-vv',
    '--debug',
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
    default=logging.WARNING,
    help="Increase output verbosity for debugging",
)

parser.add_argument(
    '-s',
    '--show-gui',
    action='store_true',
    help='Show browser window'
)

parser.add_argument(
    '-w',
    '--wrap-limit',
    type=int,
    help='Number of characters to wrap the line. Including spaces'
)

parser.add_argument(
    '-x',
    '--delete',
    action='store_true',
    help='Delete files when traslated'
)


args = parser.parse_args()
logging.basicConfig(level=args.loglevel)

if not args.show_gui:
    os.environ['MOZ_HEADLESS'] = '1'


translator = deepl.translator()

translator.translate(
    args.filepath,
    args.input_lang,
    args.output_lang,
    wrap_line_limit=args.wrap_limit,
    delete_old=args.delete
)

translator.close()