"""Module for display-related functionality."""

from lib.ili9341 import color565
from lib.xglcd_font import XglcdFont


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
