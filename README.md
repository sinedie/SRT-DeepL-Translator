# SRT-DeepL translator using Selenium

Disclaimer: 06/05/2022 - I still work on this, just dont have enough time lately. If u want to collaborate, get in touch and keep waiting for updates.

All the hard work is on the hands of the
[DeepL](https://www.deepl.com/translator) creators. I didn't do shit.

## Language support

The same support as DeepL obviously

### Input languages

    auto: Any language (detect)
    bg: Bulgarian
    zh: Chinese
    cs: Czech
    da: Danish
    nl: Dutch
    en: English
    et: Estonian
    fi: Finnish
    fr: French
    de: German
    el: Greek
    hu: Hungarian
    it: Italian
    ja: Japanese
    lv: Latvian
    lt: Lithuanian
    pl: Polish
    pt: Portuguese
    ro: Romanian
    ru: Russian
    sk: Slovak
    sl: Slovenian
    es: Spanish
    sv: Swedish

### Output languages

    bg: Bulgarian
    zh: Chinese (simplified)
    cs: Czech
    da: Danish
    nl: Dutch
    en: English
    et: Estonian
    fi: Finnish
    fr: French
    de: German
    el: Greek
    hu: Hungarian
    it: Italian
    ja: Japanese
    lv: Latvian
    lt: Lithuanian
    pl: Polish
    pt: Portuguese
    br: Portuguese (Brazilian)
    ro: Romanian
    ru: Russian
    sk: Slovak
    sl: Slovenian
    es: Spanish
    sv: Swedish

## Installation

[PyPi](https://pypi.org/project/srt-deepl/)

```
pip install srt-deepl
```

## Usage

### From python

`driver=None` use the default Firefox web driver with a random generated
free proxy from [Free Proxy List](https://free-proxy-list.net/). If you wanna
use a custom webdriver, eg with Tor, you could pass it on this argument. Check
examples folder for a hint of how would you do it.

```
from srt_deepl import translate

translate(
  filepath='./test.srt',
  lang_from='en',
  lang_to='es',
  wrap_limit=50,
  delete_old=False,
  driver=None
)
```

### Command line

#### Easy way

```
python -m srt_deepl -g
```

#### Help

```
python -m srt_deepl -h

usage: main.py [-h] [-i {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv}]
               [-o {bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,br,ro,ru,sk,sl,es,sv}] [-v] [-vv] [-g] [-s] [-w WRAP_LIMIT] [-x]
               [path]

Translates .STR files using DeepL.com

positional arguments:
  path                  Files to convert (if directory traslates all srt files recursively)

optional arguments:
  -h, --help            show this help message and exit
  -i {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv}, --input-lang {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv}
                        Language to translate from. Default: auto
  -o {bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,br,ro,ru,sk,sl,es,sv}, --output-lang {bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,it,ja,lv,lt,pl,pt,br,ro,ru,sk,sl,es,sv}
                        Language to translate to. Default: es (spanish)
  -v, --verbose         Increase output verbosity
  -vv, --debug          Increase output verbosity for debugging
  -g, --show-gui        Show configuration graphical interface
  -s, --show-browser    Show browser window
  -w WRAP_LIMIT, --wrap-limit WRAP_LIMIT
                        Number of characters to wrap the line. Including spaces. Default: 50
  -x, --delete          Delete files when traslated

```

# TODO

- Unit test
- Bug fix (if there are)
