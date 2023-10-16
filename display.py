"""Module for display-related functionality."""

from lib.ili9341 import color565
from lib.xglcd_font import XglcdFont
import urandom
import utime


COLOURS = (
    color565(255, 255, 255),  # White
    color565(0, 255, 255),    # Aqua
    color565(0, 0, 255),      # Blue
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


def strf_datetime(y, m, d, hh, mm, ss, wd=None):
    s = f'{d:02d}-{m:02d}-{y:02d} {hh:02d}:{mm:02d}:{ss:02d}'
    return s if wd is None else f'{WEEKDAYS[wd]}, ' + s


def render_datetime(lcd, ypos):
    lcd.draw_text(
        166,
        28 if ypos == 45 else 24,
        strf_datetime(*utime.localtime()[:7]),
        FONTS[1],
        COLOURS[0])


def pad_header(name, sep='~'):
    return f' {name} {sep * (44 - len(name))}'


def rjust(s, max_len=7):
    return s if len(s) == max_len else ' ' * (max_len - len(s)) + s


def render_salaah_meta(meta, lcd, ypos, on_start=True):
    if on_start:
        lcd.draw_text(0, ypos + 16, pad_header('SALAAH'), FONTS[0], COLOURS[0])

    ypos += 30
    for prayers, times in zip(PRAYERS, meta):
        lcd.draw_text(40, ypos, f'{rjust(prayers[0])}: {times[0]}', FONTS[1], COLOURS[0])
        lcd.draw_text(180, ypos, f'{rjust(prayers[1])}: {times[1]}', FONTS[1], COLOURS[0])
        ypos += 12


def generate_progress_bar(val, width=10):
    fill = round(val / 100 * width)
    return f"<{'*' * fill}" + f"{'_' * (width - fill)}>"


def render_atmospheric_meta(meta, lcd, ypos, on_start=True):
    if on_start:
        lcd.draw_text(0, ypos + 68, pad_header('ATMOSPHERE'), FONTS[0], COLOURS[0])

    lcd.draw_text(10, ypos + 82, f"{rjust('exTemp')}: {meta[0][0]}", FONTS[1], COLOURS[0])
    lcd.draw_text(180, ypos + 82, f"{rjust('inTemp')}: {meta[0][1]}", FONTS[1], COLOURS[0])
    lcd.draw_text(40, ypos + 94, f"{rjust('exFeels')}: {meta[1][0]}", FONTS[1], COLOURS[0])
    lcd.draw_text(180, ypos + 94, f"{rjust('inPres')}: {meta[1][1]}", FONTS[1], COLOURS[0])
    lcd.draw_text(40, ypos + 106, f"{rjust('exPres')}: {meta[2][0]}", FONTS[1], COLOURS[0])
    lcd.draw_text(180, ypos + 106, f"{rjust('inHumd')}: {meta[2][1]}", FONTS[1], COLOURS[0])
    lcd.draw_text(40, ypos + 118, f"{rjust('exHumd')}: {meta[3][0]}", FONTS[1], COLOURS[0])

    clouds = meta[3][1]
    lcd.draw_text(144, ypos + 118,
        f"{rjust('Clds')}: {clouds}% / {generate_progress_bar(clouds)}", FONTS[1], COLOURS[0])


def render_network_meta(meta, lcd, ypos, on_start=True):
    if on_start:
        lcd.draw_text(0, ypos + 132, pad_header('NETCONFIG'), FONTS[0], COLOURS[0])

    lcd.draw_text(6, ypos + 146,
        f"{rjust('locIP', max_len=6)}: {meta[0][0]}", FONTS[1], COLOURS[0])
    lcd.draw_text(160, ypos + 146, f"{rjust('rouIP')}: {meta[0][1]}", FONTS[1], COLOURS[0])
    lcd.draw_text(6, ypos + 158, f'locMac: {meta[1][0]}', FONTS[1], COLOURS[0])
    lcd.draw_text(160, ypos + 158, f"{rjust('rouMac')}: {meta[1][1]}", FONTS[1], COLOURS[0])
    lcd.draw_text(28, ypos + 170, f'hostname: {meta[2][0]}', FONTS[1], COLOURS[0])
    lcd.draw_text(160, ypos + 170, f'netAuth: {meta[2][1]}', FONTS[1], COLOURS[0])

    rssi = meta[3]
    rssi_pct = min(max(2 * (rssi + 100), 0), 100)    # https://stackoverflow.com/questions/15797920
    lcd.draw_text(40, ypos + 182,
        f'Signal: {rssi}dBm / {generate_progress_bar(rssi_pct, width=20)}', FONTS[1], COLOURS[0])
