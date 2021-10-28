import board
import displayio

from adafruit_display_text import label, wrap_text_to_pixels
from io_expander import IOExpander

import terminalio

WRAP_WIDTH = board.DISPLAY.width

io_expander = IOExpander(board.I2C())

about_text = (
    "The green forest of belgium has been the place \n"
    "where the secure team reunites. This is where \n"
    "COWorkers come together, hack around, play games, \n"
    "host workshops in a place were they can be their \n"
    "true self. In other words this is where the\n"
    "magic happens.\n\n"

    "A year ago, in october 2020 we attempted to gather\n"
    "the herd but where cut short of an opportunity due\n"
    "to a threat which prevented us to travel through\n"
    "space.\n"
    "This year we reinvented ourselves as SPACE COWS, a\n"
    "group of geeky cows hacking their way to the MOOOn.\n\n"

    "We are really proud to have spend many hours\n"
    "ruminating about creating a cooler badge than last\n"
    "year and we are exctactic about the result.\n"
    "This year we give you a personal rocket to bring\n"
    "you to the MOOOn!\n\n"

    "OOO 2021 Space Cows has been made possible by:\n"
    "- Cedric van Bockhaven\n"
    "- Christiaan van den Boogaard\n"
    "- Anneloes Geerts\n"
    "- James Gratchoff\n"
    "- Max Grim\n"
    "- Olaf Haalstra\n"
    "- David Haines\n"
    "- Rikkert ten Klooster\n"
    "- Pavlos Lontorfos\n"
    "With special thanks to:\n"
    "- Niels van der Vorle\n"
    "- Burc Yildirim\n"
)

about_label = None

display = board.DISPLAY
group = displayio.Group()
current_y = 10
move_speed = 340

def build_label():
    about_label = label.Label(terminalio.FONT, text="\n"\
    .join(wrap_text_to_pixels(about_text, WRAP_WIDTH, terminalio.FONT)), color=0xFFFFFF)

    about_label.anchor_point = (0.0, 0.0)
    about_label.anchored_position = (10, current_y)
    return about_label

def move_down():
    global current_y
    
    if about_label.anchored_position[1] < -100:
        return

    current_y = current_y - move_speed
    about_label.anchored_position = (10, current_y)
    
def move_up():
    global current_y
    if about_label.anchored_position[1] > 0:
        return
    current_y = current_y + move_speed
    about_label.anchored_position = (10, current_y)

def show_about(_):
    global about_label
    
    if about_label is None:
        about_label = build_label()
        group.append(about_label)

    display.show(group)

    while True:
        io_expander.update()
        if io_expander.button_down.fell:
            move_down()
        if io_expander.button_up.fell:
            move_up()        
        if io_expander.button_menu.fell or io_expander.button_b.fell:
            return
