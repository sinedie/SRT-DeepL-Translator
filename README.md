# SRT-DeepL translator using Selenium

## Installation

```
pip install srt_deepl (not yet in production. Dont use it)
```

## Usage

### From python

```
from srt_deepl import translate (not yet in production. Dont use it)
```

### Command line

#### Easy way

```
python main.py -g
```

#### Help

```
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
