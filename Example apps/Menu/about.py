import board
import displayio

from adafruit_display_text import label, wrap_text_to_pixels
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer

import terminalio

def show_about():
    io_expander = TCA9539(board.I2C())
    menu_button = Debouncer(io_expander.get_pin(15))

    font = terminalio.FONT

    WRAP_WIDTH = 320
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

    about_label = label.Label(font, text="\n"\
        .join(wrap_text_to_pixels(about_text, WRAP_WIDTH, font)), color=0xFFFFFF)

    about_label.anchor_point = (0.0, 0.0)
    about_label.anchored_position = (10, 10)

    display = board.DISPLAY
    group = displayio.Group()
    group.append(about_label)
    display.show(group)

    while True:
        io_expander.gpio_update()
        menu_button.update()

        if menu_button.fell:
            return