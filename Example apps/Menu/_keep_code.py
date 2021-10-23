import board
import displayio
import menu
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer
from adafruit_display_text import label
import terminalio
import settings
import about
import logo
import utils


def run_about(args):
    about.show_about()
    return go_to_main_menu(None)

display = board.DISPLAY
group = displayio.Group()
display.show(group)

logo_height = logo.display_logo(group, display.width / 2, 25)

main_menu_group = displayio.Group()
app_menu_group = displayio.Group()

def go_to_app_menu(args):
    group.pop()
    group.append(app_menu_group)
    return 1

def go_to_main_menu(args):
    group.pop()
    group.append(main_menu_group)
    display.show(group)
    return 0

app_menu_items = utils.get_apps_list(go_to_main_menu)

main_menu_items = [
    {"text": "Apps", "action": go_to_app_menu, "args": None},
    {"text": "Install new apps", "action": go_to_app_menu, "args": None},
    {"text": "Settings", "action": go_to_app_menu, "args": None},
    {"text": "About", "action": run_about, "args": None},
    {"text": "Test 1", "action": run_about, "args": None},
    {"text": "Test 2", "action": run_about, "args": None},
    {"text": "Test 3", "action": run_about, "args": None},
    {"text": "Test 4", "action": run_about, "args": None},
    {"text": "Test 5", "action": run_about, "args": None}
]

app_menu = menu.Menu(app_menu_items)
app_menu.initialize_labels(20, 20)

for menu_label in app_menu.labels:
    app_menu_group.append(menu_label)

main_menu = menu.Menu(main_menu_items)
main_menu.initialize_labels(20, logo_height + 20 + 20)

welcome_label = label.Label(terminalio.FONT, text="Welcome " + settings.cow_name, color=0xFFFFFF)
welcome_label.anchor_point = (0.0, 0.0)
welcome_label.anchored_position = (20, logo_height + 20)
main_menu_group.append(welcome_label)

for label in main_menu.labels:
    main_menu_group.append(label)

group.append(main_menu_group)

menus = [main_menu, app_menu]
current_menu = 0

io_expander = TCA9539(board.I2C())
down_button = Debouncer(io_expander.get_pin(9))
up_button = Debouncer(io_expander.get_pin(12))
center_button = Debouncer(io_expander.get_pin(10))
a_button = Debouncer(io_expander.get_pin(4))

while True:
    io_expander.gpio_update()
    down_button.update()
    up_button.update()
    center_button.update()
    a_button.update()

    if down_button.fell:
        active_item = menus[current_menu].menu_move(0)
        if active_item > 4:
            main_menu_group.y -= 20

    if up_button.fell:
        active_item = menus[current_menu].menu_move(1)

    if center_button.fell or a_button.fell:
        active_item = menus[current_menu].get_active_item()
        action = active_item["action"]
        current_menu = action(active_item["args"])