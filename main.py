import os
import time
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from srt import SRT


parser = argparse.ArgumentParser(
    description='Converts plain text files to docx and viceversa'
)

parser.add_argument(
    'filepath',
    metavar='path',
    type=str,
    nargs='+',
    help='File to convert'
)
parser.add_argument(
    "-v", "--verbose",
    help="increase output verbosity",
    action="store_true"
)


args = parser.parse_args()

if args.verbose:
    def verboseprint(*args):
        for arg in args:
           print(arg)
else:   
    verboseprint = lambda *a: None      # do-nothing function


verboseprint("Opening browser")
geckodriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "geckodriver"))

os.environ['MOZ_HEADLESS'] = '1'
browser = webdriver.Firefox(executable_path=geckodriver_path)

verboseprint("Going to deepl.com")
browser.get("https://www.deepl.com/translator")

verboseprint("Getting source and target inputs")
inputElement = browser.find_element_by_class_name("lmt__source_textarea")
targetElement = browser.find_element_by_class_name("lmt__target_textarea")

def traslate_srt(file_in, file_out):

    verboseprint("\n" + "=" * 50)
    verboseprint(f"File to traslate {file_in}")
    verboseprint("=" * 50)
    # Opening file
    srt_file = SRT(file_in)

    sub_id = 0  # ID of initial subtitle
    while sub_id < srt_file.n_subtitles:

        verboseprint("Clearing input")

        # Clearing input
        inputElement.clear()
        
        traslation = targetElement.get_attribute('value')

        while len(traslation) != 0:
            time.sleep(1)
            traslation = targetElement.get_attribute('value')


        verboseprint("Getting next portion")

        # Portion to of srt to traslate
        text, sub_id_f = srt_file.extract_portion(sub_id)


        verboseprint("Writing portion on input")

        # Sending text
        inputElement.send_keys(text)

        verboseprint("Traslating portion")

        # Getting traslation
        traslation = targetElement.get_attribute('value')

        while not traslated(text, traslation):
            time.sleep(1)
            traslation = targetElement.get_attribute('value')

        traslation = targetElement.get_attribute('value').splitlines()

        verboseprint("Saving portion")

        # Updation text on SRT
        srt_file.update_text(sub_id, traslation)

        # Getting next portion
        sub_id = sub_id_f

    # Saving file
    verboseprint("Wraping lines")
    srt_file.wrap_lines()
    verboseprint(f"Saving {file_out}")
    srt_file.save(file_out)


def traslated(text, traslation):

    if len(traslation) == 0:
        return False
    elif len(text.splitlines()) != len(traslation.splitlines()):
        return False
    elif "[...]" in traslation:
        return False

    return True


def traslate_all(file_paths):

    for path in file_paths:

        if not os.path.exists(path):
            print(f"File '{path}' doesn't exist, skipping...")
            continue
        
        if os.path.isdir(path):
            for file_path in [os.path.join(path, file_path) for file_path in os.listdir(path)]:
                if not os.path.isdir(file_path):
                    traslate_srt(file_path, os.path.splitext(file_path)[0] + "_traslated.srt")
        else:
            traslate_srt(path, os.path.splitext(path)[0] + ".srt")

traslate_all(args.filepath)

browser.quit()