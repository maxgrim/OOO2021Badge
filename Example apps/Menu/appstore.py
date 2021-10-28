import wifi
import socketpool
import ssl
import adafruit_requests
import menu
import board
import displayio
from adafruit_display_text import label
import terminalio
from io_expander import IOExpander
import settings
import storage
import os
import utils
import time


root_menu = menu.Menu()
menu_collection = menu.MenuCollection(root_menu)
d_group_root = displayio.Group()

status_label = label.Label(terminalio.FONT, text="Loading...")
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)

appstore_data = {}

socket_pool = None
request_session = None

def go_menu_back(args):
    # Remove the last menu
    d_group_root.pop()
    menu_collection.pop_menu()
    d_group_root.append(menu_collection.active_menu.display_group)

def connect_wifi():
    try:
        wifi.radio.connect(
            ssid=settings.wifi_ssid, 
            password=settings.wifi_psk
        )
        return True
    except ConnectionError:
        return False

def install_app(args):
    for _ in range(len(d_group_root)):
        d_group_root.pop()
    
    status_label.text = "Installing app"
    d_group_root.append(status_label)

    app = args["app"]

    url = "{0}/api.php?path={1}&act=getapp&name={2}".format(
        settings.appstore_base_url,
        app["path"],
        app["name"]
    )

    response = request_session.request(
        "GET", 
        url,
        headers=settings.appstore_backdoor_header)
    response_data = response.json()

    existing_apps = os.listdir("/apps")
    if app["name"] in existing_apps:
        status_label.text = "Removing current version"
        utils.delete_folder_recursive("/apps/" + app["name"])

    status_label.text = "Creating directories"
    os.mkdir("{0}/{1}".format("/apps", app["name"]))

    for file_entry in response_data["filelist"]:
        if file_entry["type"] != "folder":
            continue

        if file_entry["relpath"] == "lib":
            continue

        os.mkdir("{0}/{1}/{2}".format("/apps", app["name"], file_entry["relpath"]))
    
    os.sync()

    for i, file_entry in enumerate(response_data["filelist"]):
        status_label.text = "Downloading file ({0}/{1})".format(i + 1, len(response_data["filelist"]))

        if file_entry["type"] == "file":
            url = "{0}/{1}".format(
                settings.appstore_base_url,
                file_entry["path"],
                app["path"]
            )

            response = request_session.request(
                "GET", 
                url,
                headers=settings.appstore_backdoor_header)

            if file_entry["path"].startswith("lib/"):
                file_entry["path"] = "/" + file_entry["path"]

            status_label.text = "Writing file ({0}/{1})".format(i + 1, len(response_data["filelist"]))
            f = open("/apps/" + app["name"] + "/" + file_entry["relpath"], "wb")
            f.write(response.content)
            f.close()

    status_label.text = "App installed!"
    status_label.color = 0x00FF00
    time.sleep(2)
    status_label.color = 0xFFFFFF

    os.sync()
    d_group_root.pop()
    d_group_root.append(menu_collection.active_menu.display_group)

def build_app_overview_menu(args):
    # Remove the last menu
    d_group_root.pop()

    app = args["app"]

    app_overview_menu = menu.Menu()
    app_overview_menu.add_entry(menu.MenuLabelEntry("Install", utils.run_list, {
        "run_actions": [install_app, go_menu_back],
        "run_args": [{"app": app}, None]
    }))

    app_overview_menu.add_entry(menu.MenuLabelEntry("Go back", go_menu_back, None))
    
    menu_collection.push_menu(app_overview_menu, "app_overview_menu")
    d_group_root.append(menu_collection.active_menu.display_group)

def build_category_menu(args):
    # Remove the last menu
    d_group_root.pop()

    category_menu = menu.Menu()

    for app in appstore_data[args["category_name"]]:
        title = app["title"]
        if utils.is_app_installed(app["name"]):
            title = title + " (installed)"
        category_menu.add_entry(menu.MenuLabelEntry(title, build_app_overview_menu, {"app": app}))

    category_menu.add_entry(menu.MenuLabelEntry("Go back", go_menu_back, None))

    menu_collection.push_menu(category_menu, "category_menu")
    d_group_root.append(menu_collection.active_menu.display_group)

def get_appstore_data():
    status_label.text = "Downloading app list..."
    response = request_session.request(
        "GET", 
        "https://store.spacecows.nl/api.php",
        headers=settings.appstore_backdoor_header)

    response_data = response.json()

    for (path, path_obj) in response_data["paths"].items():
        appstore_data[path] = []

        if path == "usercontent":
            for (author, author_obj) in path_obj["paths"].items():
                for app in author_obj["apps"]:
                    app["path"] = "{0}/{1}".format(path, author)
                    appstore_data[path].append(app)
        else:
            for app in path_obj["apps"]:
                app["path"] = path
                appstore_data[path].append(app)


should_exit = False

def exit_run_store(_):
    global should_exit
    should_exit = True

def run_store(_):
    global socket_pool, request_session

    socket_pool = socketpool.SocketPool(wifi.radio)
    request_session = adafruit_requests.Session(
        socket_pool, ssl.create_default_context())
    io_expander = IOExpander(board.I2C())

    display = board.DISPLAY
    d_group_root.append(status_label)
    display.show(d_group_root)

    try:
        storage.remount("/", False)
    except RuntimeError:
        status_label.text = "USB drive has to be ejected"
        # TODO fix this
        while True:
            pass

    status_label.text = "Connecting to WiFi..."

    if not connect_wifi():
        status_label.text = "Failed to connect! :("
        while True:
            pass

    get_appstore_data()

    for category in appstore_data:
        root_menu.add_entry(menu.MenuLabelEntry(category, build_category_menu, {
            "category_name": category
        }))

    root_menu.add_entry(menu.MenuLabelEntry("Go back", exit_run_store, None))

    d_group_root.remove(status_label)
    d_group_root.append(root_menu.display_group)

    while not should_exit:
        io_expander.update()

        if io_expander.button_down.fell:
            menu_collection.active_menu.move_down()

        if io_expander.button_up.fell:
            menu_collection.active_menu.move_up()

        if io_expander.button_center.fell or io_expander.button_a.fell:
            selected_item = menu_collection.active_menu.selected_item
            selected_item.execute_action()

        if io_expander.button_menu.fell or io_expander.button_b.fell:
            if len(menu_collection.menus) == 1:
                return
            else:
                go_menu_back(None)
