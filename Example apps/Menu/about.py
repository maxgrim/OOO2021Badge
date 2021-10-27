import board
import displayio

from adafruit_display_text import label, wrap_text_to_pixels
from io_expander import IOExpander

import terminalio

WRAP_WIDTH = 320

io_expander = IOExpander(board.I2C())

about_text = (
    "OOO 2021 Space Cows has been made possible by:\n\n"
    "- Christiaan van den Boogaard\n"
    "- Anneloes Geerts\n"
    "- James Gratchoff\n"
    "- Max Grim\n"
    "- Olaf Haalstra\n"
    "- David Haines\n"
    "- Rikkert ten Klooster\n"
    "- Pavlos Lontorfos\n"
    "\nWith special thanks to:\n"
    "- Niels van der Vorle\n"
    "- Burc Yildirim\n"
)

about_label = None

display = board.DISPLAY
group = displayio.Group()

def build_label():
    about_label = label.Label(terminalio.FONT, text="\n"\
    .join(wrap_text_to_pixels(about_text, WRAP_WIDTH, terminalio.FONT)), color=0xFFFFFF)

    about_label.anchor_point = (0.0, 0.0)
    about_label.anchored_position = (10, 10)
    return about_label

def show_about(_):
    global about_label
    
    if about_label is None:
        about_label = build_label()
        group.append(about_label)

    display.show(group)

    while True:
        io_expander.update()

        if io_expander.button_menu.fell:
            return