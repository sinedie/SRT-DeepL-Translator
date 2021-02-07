# SRT-DeepL translator using Selenium

## Usage
```
main.py [-h] [-v] [-vv] [-s] [-i {language}] [-o {language}] path [path ...]

Traslate a .SRT file using DeepL and Selenium

positional arguments:
    path: File to convert

optional arguments:
    -h, --help: Show this help message and exit
    -v, --verbose: Increase output verbosity
    -vv, --debug: Increase output verbosity for debugging
    -s: Show browser window
    -i, --input-lang: Language to translate from
        choices: { auto, chinese, dutch, english, french, german, italian, japanese, polish, portuguese, russian, spanish }
    -o, --output-lang: Language to translate to
        choices: { chinese, dutch, english-us, english-uk, french, german, italian, japanese, polish, portuguese, portuguese-br, russian, spanish}
```

## Setup
use ```pip install -r requirements.txt``` or ```execute setup.sh```

### Geckodriver version

Geckodriver -v0.24.0

## Features to add
- Use voice recognition to generate the subtitles
- Use OCR to extract forced subtitles
