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
import battery
import digitalio
from analogio import AnalogIn
import adafruit_imageload
from adafruit_display_text import label, wrap_text_to_pixels
from io_expander import IOExpander
import os
import update


display = board.DISPLAY
analog_in = AnalogIn(board.SENSE_BATT)
usb = digitalio.DigitalInOut(board.SENSE_USB)
usb.direction = digitalio.Direction.INPUT

d_group_root = displayio.Group()
d_group_logo = displayio.Group()

d_group_root.append(d_group_logo)

display.show(d_group_root)

screensaver_time = time.monotonic()

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/img/batteries.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

battery_group = displayio.Group(scale=3)
# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=9,
                            tile_height=4)
battery_group.append(sprite)
battery_group.x = display.width - 30
d_group_root.append(battery_group)

logo_height = logo.display_logo(d_group_logo, display.width / 2, 25)

name_label = label.Label(terminalio.FONT, text="Welcome " + settings.cow_name() + "!", color=0xFF0000)
name_label.anchor_point = (0.5, 0.0)
name_label.anchored_position = (display.width / 2, logo_height + 10)
d_group_logo.append(name_label)


loading_group = displayio.Group()
loading_label = label.Label(terminalio.FONT, text="Loading...", color=0xFF0000)
loading_label.anchor_point = (0.5, 0.5)
loading_label.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)
loading_group.append(loading_label)


def go_menu_back(args):
    # Remove the last menu
    d_group_root.pop()
    menu_collection.pop_menu()
    d_group_root.append(menu_collection.active_menu.display_group)

def show_logo(args):
    d_group_root.append(d_group_logo)

def hide_logo(args):
    d_group_root.remove(d_group_logo)

def build_apps_menu(_):
    # Remove the last menu
    d_group_root.pop()

    hide_logo(None)

    apps_menu = menu.Menu()
    for app in utils.get_apps_list():
        apps_menu.add_entry(
            menu.MenuLabelEntry(app["name"], utils.run_and_display, {
                "actions": [utils.start_app, show_logo],
                "actions_args": [{"app": app}, None],
                "display_before": loading_group,
                "display_after": d_group_root
            }))

    apps_menu.add_entry(menu.MenuLabelEntry("Go back", go_menu_back, None))
    menu_collection.push_menu(apps_menu, "apps_menu")
    d_group_root.append(menu_collection.active_menu.display_group)

root_menu = menu.Menu(start_y=logo_height + name_label.height + 20)

root_menu.add_entry(menu.MenuLabelEntry("Apps", build_apps_menu, None))
root_menu.add_entry(menu.MenuLabelEntry("Install new apps", utils.run_and_display, {
    "actions": [appstore.run_store],
    "actions_args": [None],
    "display_after": d_group_root
}))

# TODO: implement
# root_menu.add_entry(menu.MenuLabelEntry("Settings", None, None))
root_menu.add_entry(menu.MenuLabelEntry("About", utils.run_and_display, {
    "actions": [about.show_about],
    "actions_args": [None],
    "display_before": loading_group,
    "display_after": d_group_root
}))

root_menu.add_entry(menu.MenuLabelEntry("Update firmware", utils.run_and_display, {
    "actions": [update.main],
    "actions_args": [None],
    "display_before": loading_group,
    "display_after": d_group_root
}))


d_group_root.append(root_menu.display_group)
menu_collection = menu.MenuCollection(root_menu)

io_expander = IOExpander(board.I2C())

def reset_screensaver_time():
    global screensaver_time
    screensaver_time = time.monotonic()

def play_intro():
    if utils.has_intro_played():
        return
    
    apps = utils.get_apps_list()
    intro_app = None

    for app in apps:
        if app["name"] == "Intro":
            intro_app = app
            break
    
    if intro_app is not None:
        utils.run_and_display({
            "actions": [utils.start_app],
            "actions_args": [{"app": app}],
            "display_before": loading_group,
            "display_after": d_group_root
        })

        utils.set_intro_played()
    
    reset_screensaver_time()

play_intro()

while True:
    io_expander.update()
    battery.get_battery_percentage(sprite, analog_in.value, usb.value)

    if io_expander.any_button_fell:
        reset_screensaver_time()

    if io_expander.button_down.fell:
        menu_collection.active_menu.move_down()

    if io_expander.button_up.fell:
        menu_collection.active_menu.move_up()

    if io_expander.button_center.fell or io_expander.button_a.fell:
        selected_item = menu_collection.active_menu.selected_item
        selected_item.execute_action()
        reset_screensaver_time()

    if io_expander.button_menu.fell or io_expander.button_b.fell:
        go_menu_back(None)

    if time.monotonic() > screensaver_time + settings.screensaver_timeout:
        utils.screensaver()
        reset_screensaver_time()
        display.show(d_group_root)