"""Module for display-related functionality."""

from lib.ili9341 import color565


COLOURS = [
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
]

TITLES = [
    '''
 _  ___   __   ___  ___  
|\|| |_) / /\ | _ \| _ \ 
|_||_|  /_/--\|___/|___/ 
''',
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
]
