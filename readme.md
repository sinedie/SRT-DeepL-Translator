# SRT-DeepL translator using Selenium

## Usage
```
main.py [-h] [-v] [-vv] [-s] [-i {language}] [-o {language}] [-w WRAP_LIMIT] [-x] path [path ...]

Traslate a .SRT file using DeepL and Selenium

positional arguments:
    path: Files to convert (if directory traslates all srt files recursively)

optional arguments:
    -h, --help: Show this help message and exit
    -v, --verbose: Increase output verbosity
    -vv, --debug: Increase output verbosity for debugging
    -s: Show browser window
    -i, --input-lang: Language to translate from. Default: auto
        choices: { auto, chinese, dutch, english, french, german, italian, japanese, polish, portuguese, russian, spanish }
    -o, --output-lang: Language to translate to. Default: spanish
        choices: { chinese, dutch, english-us, english-uk, french, german, italian, japanese, polish, portuguese, portuguese-br, russian, spanish}
    -x, --delete: Delete files when traslated
    -w WRAP_LIMIT, --wrap-limit WRAP_LIMIT: Number of characters to wrap the line. Including spaces. Default: 20
```

## Setup
use ```pip install -r requirements.txt``` or ```execute setup.sh```

### Geckodriver version

Geckodriver -v0.24.0

## Features to add
- Use voice recognition to generate the subtitles
- Use OCR to extract forced subtitles
