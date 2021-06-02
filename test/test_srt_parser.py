from srt import Subtitle
import datetime
from srt_deepl.srt_parser import wrap_line, get_srt_portions

def test_wrap_line():
    
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum orci nisi, convallis eget iaculis ac, tincidunt vel elit. tincidunt vel elit.....'
    max_char = 50
    
    wraped_line = wrap_line(text, max_char)
    
    assert len(text.split()) == len(' '.join(wraped_line.split('\n')).split())
    assert wraped_line == 'Lorem ipsum dolor sit amet, consectetur adipiscing\nelit. Vestibulum orci nisi, convallis eget iaculis\nac, tincidunt vel elit. tincidunt vel elit.....'
    assert len(wraped_line.split('\n')) == 3
    for line in wraped_line.split('\n'):
        assert len(line) <= max_char


def test_get_srt_portions():
    
    subtitles = [
        Subtitle(1, datetime.timedelta(0, 1), datetime.timedelta(0, 2), 'TEST0'),
        Subtitle(1, datetime.timedelta(0, 1), datetime.timedelta(0, 2), 'TEST1'),
        Subtitle(1, datetime.timedelta(0, 1), datetime.timedelta(0, 2), 'TEST2'),
        Subtitle(1, datetime.timedelta(0, 1), datetime.timedelta(0, 2), 'TEST3'),
    ]
    
    characters = 11
    portions = list(get_srt_portions(subtitles, characters))
    assert len(portions) == 2
    for portion in portions:
        assert len(portion) != 0
        assert sum(len(sub.content) for sub in portion) < characters
        
    characters = 10
    portions = list(get_srt_portions(subtitles, characters))
    assert len(portions) == 4
    for portion in portions:
        assert len(portion) != 0
        assert sum(len(sub.content) for sub in portion) < characters
        
    characters = 6
    portions = list(get_srt_portions(subtitles, characters))
    assert len(portions) == 4
    for portion in portions:
        assert len(portion) != 0
        assert sum(len(sub.content) for sub in portion) < characters