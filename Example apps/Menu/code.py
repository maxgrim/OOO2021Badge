import wifi
import socketpool
import ssl
import adafruit_requests
import menu
import board
import displayio
from adafruit_display_text import label, wrap_text_to_pixels
import terminalio
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer
import settings


def connect_wifi():
    try:
        wifi.radio.connect(
            ssid=settings.wifi_ssid, 
            password=settings.wifi_psk
        )
        return True
    except ConnectionError:
        return False

socket_pool = socketpool.SocketPool(wifi.radio)
request_session = adafruit_requests.Session(
    socket_pool, ssl.create_default_context())

backdoor_header = {"X-Badge-Backdoor": "spacecows"}

display = board.DISPLAY
main_group = displayio.Group()
display.show(main_group)

status_label = label.Label(terminalio.FONT, text="Connecting to WiFi...")
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (display.width / 2, display.height / 2)
main_group.append(status_label)

if not connect_wifi():
    status_label.text = "Failed to connect! :("
    while True:
        pass

status_label.text = "Downloading app list..."
response = request_session.request(
    "GET", 
    "https://store.spacecows.nl/api.php",
    headers=backdoor_header)

response_data = response.json()

main_group.remove(status_label)

appstore_data = {}

for (path, path_obj) in response_data["paths"].items():
    appstore_data[path] = []

    if path == "usercontent":
        for (author, author_obj) in path_obj["paths"].items():
            for app in author_obj["apps"]:
                appstore_data[path].append(app)
    else:
        for app in path_obj["apps"]:
            appstore_data[path].append(app)

menu_stack = ["main_menu"]
menus = {
    "main_menu": menu.Menu()
}

def menu_active():
    return menus[menu_stack[-1]]

def menu_launch(name, menu):
    menus[name] = menu

    main_group.remove(menu_active().display_group)
    menu_stack.append(name)
    main_group.append(menu_active().display_group)

def menu_back():
    if len(menu_stack) == 1:
        return

    main_group.remove(menu_active().display_group)
    menu_stack.pop()
    main_group.append(menu_active().display_group)

def jump_to_app_details_menu(args):
    app = args[0]

    text = (
        "Title:" + app["title"] + "\n" +
        "Name:" + app["name"] + "\n" +
        "Author:" + app["author"] + "\n" +
        "Description:" + app["author"]
    )

    app_details_menu = menu.Menu(heading=text)
    app_details_menu.add_label("Install", None, None)
    app_details_menu.add_label("Back", menu_back, None)

    menu_launch("app_details_menu", app_details_menu)

def jump_to_category_menu(args):
    category = args[0]

    game_menu = menu.Menu()
    for app in appstore_data[category]:
        game_menu.add_label(
            app["title"] + " (by " + app["author"] + ")",
            jump_to_app_details_menu, [app])

    menu_launch("game_menu", game_menu)

for category in appstore_data:
    menus["main_menu"].add_label(category, jump_to_category_menu, [category])

main_group.append(menus["main_menu"].display_group)

io_expander = TCA9539(board.I2C())
down_button = Debouncer(io_expander.get_pin(9))
up_button = Debouncer(io_expander.get_pin(12))
center_button = Debouncer(io_expander.get_pin(10))
a_button = Debouncer(io_expander.get_pin(4))
b_button = Debouncer(io_expander.get_pin(5))

while True:
    io_expander.gpio_update()
    down_button.update()
    up_button.update()
    center_button.update()
    a_button.update()
    b_button.update()

    if down_button.fell:
        menu_active().menu_down()

    if up_button.fell:
        menu_active().menu_up()

    if center_button.fell or a_button.fell:
        selected_item = menu_active().menu_select()
        
        # Call function for menu
        selected_item["action"](selected_item["action_args"])
    
    if b_button.fell:
        menu_back()