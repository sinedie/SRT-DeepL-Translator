# SRT-DeepL translator using Selenium

# I thought that it would be better if you can choose your translator, so all future work will be directed to: https://github.com/sinedie/SRTranslator. Check it out

If u want to collaborate, get in touch and keep waiting for updates.

All the hard work is on the hands of the
[DeepL](https://www.deepl.com/translator) creators. I didn't do shit.

## Language support

The same support as DeepL obviously

### Languages

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
    id : Indonesian
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
    tr : Turkish
    uk : Ukrainian

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

usage: main.py [-h] [-i {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv,tr,uk}]
                   [-o {bg,zh,cs,da,nl,en-US,en-GB,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt-PT,pt-BR,ro,ru,sk,sl,es,sv,tr,uk}] [-v] [-vv] [-g] [-s] [-w WRAP_LIMIT] [-x]
                   [path]

Translates .STR files using DeepL.com

positional arguments:
  path                  Files to convert (if directory traslates all srt files recursively)

optional arguments:
  -h, --help            show this help message and exit
  -i {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv,tr,uk}, --input-lang {auto,bg,zh,cs,da,nl,en,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt,ro,ru,sk,sl,es,sv,tr,uk}
                        Language to translate from. Default: auto
  -o {bg,zh,cs,da,nl,en-US,en-GB,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt-PT,pt-BR,ro,ru,sk,sl,es,sv,tr,uk}, --output-lang {bg,zh,cs,da,nl,en-US,en-GB,et,fi,fr,de,el,hu,id,it,ja,lv,lt,pl,pt-PT,pt-BR,ro,ru,sk,sl,es,sv,tr,uk}
                        Language to translate to. Default: es (spanish)
  -v, --verbose         Increase output verbosity
  -vv, --debug          Increase output verbosity for debugging
  -g, --show-gui        Show configuration graphical interface
  -s, --show-browser    Show browser window
  -w WRAP_LIMIT, --wrap-limit WRAP_LIMIT
                        Number of characters to wrap the line. Including spaces. Default: 50

```
