"""Module for display-related functionality."""

from lib.ili9341 import color565
from lib.xglcd_font import XglcdFont
import urandom
import utime


COLOURS = (
    color565(255, 255, 255),  # White
    color565(0, 255, 255),    # Aqua
    color565(0, 0, 255),      # Blue
    color565(128, 255, 255),  # Cyan
    color565(0, 128, 0),      # Green (dark)
    color565(255, 0, 128),    # Pink (dark)
    color565(0, 255, 0),      # Green
    color565(0, 0, 128),      # Navy
    color565(255, 128, 0),    # Orange
    color565(128, 0, 128),    # Purple
    color565(0, 128, 128),    # Teal
    color565(255, 255, 0)     # Yellow
)

TITLES = (
    '''
 _              _    _ 
<_> ___  ___  _| | _| |
| || _ \/ _ |/ _ |/ _ |
|_||  _/\___|\___|\___|
   |_|                 
''',
    '''
 o               _    _
 _  __   ___   __)) __))
(( ((_) ((_(( ((_( ((_(
    ))
''',
    '''
 _              _    _ 
(_) ___  ___  _| | _| |
| || _ || _ || _ || _ |
|_||  _||__,||___||___|
   |_|
'''
)

FONTS = (
    XglcdFont('lib/fonts/Bally7x9.c', 7, 9),    # Header font
    XglcdFont('lib/fonts/Fixed5x8.c', 5, 8)     # Regular font
)

WEEKDAYS = (
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

PRAYERS = (
    ('Fajr', 'Asr'), ('Sunrise', 'Maghrib'), ('Dhuhr', 'Ishaa'))


def render_title(lcd):
    # Random title design chosen; white excluded from colour options
    title = list(enumerate(urandom.choice(TITLES).splitlines()))[1:]
    colour = urandom.choice(COLOURS[1:])
    for i, line in title:
        lcd.draw_text(8, (i * 9), line, FONTS[1], colour)

    return len(title) * 9


def render_datetime(lcd, ypos):
    now = utime.localtime()
    lcd.draw_text(
        166,
        28 if ypos == 45 else 22,
        f'{WEEKDAYS[now[6]]}, {now[2]:02d}-{now[1]:02d}-{now[0]}'
        + f' {now[3]:02d}:{now[4]:02d}:{now[5]:02d}',
        FONTS[1],
        COLOURS[0])


def pad_header(name, sep='~'):
    return f' {name} {sep * (44 - len(name))}'


def render_salaah_meta(meta, lcd, ypos, on_start=True):
    if on_start:
        lcd.draw_text(0, ypos + 16, pad_header('SALAAH'), FONTS[0], COLOURS[0])

    # Abstract `str.rjust` implementation for right-alignment on strings
    rjust = lambda s: s if len(s) == 7 else ' ' * (7 - len(s)) + s

    ypos += 30
    for prayers, times in zip(PRAYERS, meta):
        lcd.draw_text(
            40,
            ypos,
            f'{rjust(prayers[0])}: {times[0]}',
            FONTS[1],
            COLOURS[0])
        lcd.draw_text(
            180,
            ypos,
            f'{rjust(prayers[1])}: {times[1]}',
            FONTS[1],
            COLOURS[0])
        ypos += 12
