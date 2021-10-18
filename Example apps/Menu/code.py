import board
import displayio
import menu
import logo
import os
import supervisor
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer

supervisor.disable_autoreload()

ignored_items = [".DS_Store", "._.DS_Store"]

def start_app(args):
    # Go into module path
    os.chdir(args[1])

    module = __import__("apps." + args[0])
    my_class = getattr(module, args[0])
    my_class.main()

    # Go back to root folder
    os.chdir("/")
    
    return go_to_main_menu(None)

def get_apps_list():
    apps_items = os.listdir("/apps")
    apps_list = []

    for item in sorted(apps_items):
        if item in ignored_items:
            continue

        path = "/apps/" + item
        stat = os.stat(path)

        if stat[0] & 0x4000:
            # Directory
            # TODO: Read manifest
            # - Title
            # - BMP icon
            # - Category (?)
            # - Author
            # - Description

            apps_list.append({
                "text": item, 
                "action": start_app,
                "args": [item, path]
            })

    return apps_list

display = board.DISPLAY
group = displayio.Group()
display.show(group)

logo_tuple = logo.load_logo()
logo.display_logo(group, logo_tuple, 
    int(board.DISPLAY.width / 2 - (logo_tuple[0].width / 2)), 10)

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

app_menu_items = get_apps_list()

main_menu_items = [
    {"text": "Apps", "action": go_to_app_menu, "args": None},
    {"text": "Install new apps", "action": go_to_app_menu, "args": None},
    {"text": "Settings", "action": go_to_app_menu, "args": None},
    {"text": "Check for updates", "action": go_to_app_menu, "args": None},
    {"text": "About", "action": go_to_app_menu, "args": None},
    {"text": "Deep sleep", "action": go_to_app_menu, "args": None}
]

app_menu = menu.Menu(app_menu_items)
app_menu.initialize_labels(20, logo_tuple[0].height + 20)

for label in app_menu.labels:
    app_menu_group.append(label)

main_menu = menu.Menu(main_menu_items)
main_menu.initialize_labels(20, logo_tuple[0].height + 20)

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
        menus[current_menu].menu_move(0)

    if up_button.fell:
        menus[current_menu].menu_move(1)

    if center_button.fell or a_button.fell:
        active_item = menus[current_menu].get_active_item()
        action = active_item["action"]
        current_menu = action(active_item["args"])