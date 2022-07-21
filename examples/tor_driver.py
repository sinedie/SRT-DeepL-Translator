import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem

from srt_deepl import translate

filepath = "/path/to/str"
lang_from = "lang_from"
lang_to = "lang_to"
tbb_dir = "/path/to/TorBrowserBundle/"

tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)
with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM) as driver:
    translate(
        filepath,
        lang_from,
        lang_to,
        wrap_limit=50,
        driver=driver,
    )

tor_process.kill()
