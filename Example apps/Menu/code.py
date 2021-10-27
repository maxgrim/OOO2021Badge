import board
import displayio
import menu
import about
import logo
import appstore
import utils
import time
import settings
import terminalio

from adafruit_display_text import label, wrap_text_to_pixels
from io_expander import IOExpander

display = board.DISPLAY
d_group_root = displayio.Group()
display.show(d_group_root)

logo_height = logo.display_logo(d_group_root, display.width / 2, 25)

name_label = label.Label(terminalio.FONT, text="Welcome " + settings.cow_name() + "!", color=0xFF0000)
name_label.anchor_point = (0.5, 0.0)
name_label.anchored_position = (display.width / 2, logo_height + 10)
d_group_root.append(name_label)

loading_group = displayio.Group()
loading_label = label.Label(terminalio.FONT, text="Loading...", color=0xFF0000)
loading_label.anchor_point = (0.5, 0.5)
loading_label.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
loading_group.append(loading_label)

def go_menu_back():
    # Remove the last menu
    d_group_root.pop()
    menu_collection.pop_menu()
    d_group_root.append(menu_collection.active_menu.display_group)

def build_apps_menu(_):
    # Remove the last menu
    d_group_root.pop()

    apps_menu = menu.Menu(start_y=logo_height + name_label.height + 20)
    for app in utils.get_apps_list():
        apps_menu.add_entry(
            menu.MenuLabelEntry(app["name"], utils.run_and_display, {
                "action": utils.start_app,
                "action_args": {"app": app},
                "display_before": loading_group,
                "display_after": d_group_root
            }))

    menu_collection.push_menu(apps_menu, "apps_menu")
    d_group_root.append(menu_collection.active_menu.display_group)

root_menu = menu.Menu(start_y=logo_height + name_label.height + 20)

root_menu.add_entry(menu.MenuLabelEntry("Apps", build_apps_menu, None))
root_menu.add_entry(menu.MenuLabelEntry("Install new apps", utils.run_and_display, {
    "action": appstore.run_store,
    "action_args": None,
    "display_after": d_group_root
}))

root_menu.add_entry(menu.MenuLabelEntry("Settings", None, None))
root_menu.add_entry(menu.MenuLabelEntry("About", utils.run_and_display, {
    "action": about.show_about,
    "action_args": None,
    "display_before": loading_group,
    "display_after": d_group_root
}))

d_group_root.append(root_menu.display_group)
menu_collection = menu.MenuCollection(root_menu)

io_expander = IOExpander(board.I2C())

last_button_time = time.monotonic()

while True:
    io_expander.update()

    if io_expander.any_button_fell:
        last_button_time = time.monotonic()

    if io_expander.button_down.fell:
        menu_collection.active_menu.move_down()

    if io_expander.button_up.fell:
        menu_collection.active_menu.move_up()

    if io_expander.button_center.fell or io_expander.button_a.fell:
        selected_item = menu_collection.active_menu.selected_item
        selected_item.execute_action()

    if io_expander.button_menu.fell:
        go_menu_back()

    if time.monotonic() > last_button_time + settings.screensaver_timeout:
        utils.screensaver()
        last_button_time = time.monotonic()
        display.show(d_group_root)