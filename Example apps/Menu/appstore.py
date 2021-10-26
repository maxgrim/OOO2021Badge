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



root_menu = menu.Menu()
menu_collection = menu.MenuCollection(root_menu)
d_group_root = displayio.Group()

status_label = label.Label(terminalio.FONT, text="Loading...")
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)

appstore_data = {}

socket_pool = None
request_session = None


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
        print("app exists, removing")
        utils.delete_folder_recursive("/apps/" + app["name"])
    
    print("creating directory {0}/{1}".format("/apps", app["name"]))
    os.mkdir("{0}/{1}".format("/apps", app["name"]))

    for file_entry in response_data["filelist"]:
        if file_entry["type"] != "folder":
            continue

        print("creating directory {0}/{1}/{2}".format("/apps", app["name"], file_entry["relpath"]))
        os.mkdir("{0}/{1}/{2}".format("/apps", app["name"], file_entry["relpath"]))
    
    os.sync()

    for file_entry in response_data["filelist"]:
        print("Contents for " + file_entry["relpath"])
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

            print("Creating /apps/{0}/{1}".format(app["name"], file_entry["relpath"]))

            f = open("/apps/" + app["name"] + "/" + file_entry["relpath"], "wb")
            f.write(response.content)
            f.close()
    
    os.sync()


def build_category_menu(args):
    # Remove the last menu
    d_group_root.pop()

    category_menu = menu.Menu()
    
    for app in appstore_data[args["category_name"]]:
        category_menu.add_entry(menu.MenuLabelEntry(app["title"], install_app, {"app": app}))
    
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

    d_group_root.remove(status_label)
    d_group_root.append(root_menu.display_group)

    while True:
        io_expander.update()

        if io_expander.button_down.fell:
            menu_collection.active_menu.move_down()

        if io_expander.button_up.fell:
            menu_collection.active_menu.move_up()

        if io_expander.button_center.fell or io_expander.button_a.fell:
            selected_item = menu_collection.active_menu.selected_item
            selected_item.execute_action()


# # def jump_to_app_details_menu(args):
# #     app = args[0]

# #     text = (
# #         "Title: " + app["title"] + "\n" +
# #         "Name: " + app["name"] + "\n" +
# #         "Author: " + app["author"] + "\n" +
# #         "Description: " + app["author"]
# #     )

# #     app_details_menu = menu.Menu(heading=text)
# #     app_details_menu.add_label("Install", install_app, [app])
# #     app_details_menu.add_label("Go back", menu_back, None)

# #     menu_launch("app_details_menu", app_details_menu)

# # def jump_to_category_menu(args):
# #     category = args[0]

# #     game_menu = menu.Menu()
# #     for app in appstore_data[category]:
# #         game_menu.add_label(
# #             app["title"] + " (by " + app["author"] + ")",
# #             jump_to_app_details_menu, [app])

# #     game_menu.add_label("Go back", menu_back, None)
# #     menu_launch("game_menu", game_menu)


# main_group.append(menus["main_menu"].display_group)

# io_expander = TCA9539(board.I2C())
# down_button = Debouncer(io_expander.get_pin(9))
# up_button = Debouncer(io_expander.get_pin(12))
# center_button = Debouncer(io_expander.get_pin(10))
# a_button = Debouncer(io_expander.get_pin(4))
# b_button = Debouncer(io_expander.get_pin(5))

# while True:
#     io_expander.gpio_update()
#     down_button.update()
#     up_button.update()
#     center_button.update()
#     a_button.update()
#     b_button.update()

#     if down_button.fell:
#         menu_active().menu_down()

#     if up_button.fell:
#         menu_active().menu_up()

#     if center_button.fell or a_button.fell:
#         selected_item = menu_active().menu_select()
        
#         # Call function for menu
#         selected_item["action"](selected_item["action_args"])
    
#     if b_button.fell:
#         menu_back(None)