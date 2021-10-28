import os
import board
import adafruit_imageload
import displayio
import random
import microcontroller

from io_expander import IOExpander
from micropython import const

NVM_INDEX_INTRO_PLAYED = const(0)

ignored_items = [".DS_Store", "._.DS_Store"]

def start_app(args):
    app = args["app"]
    # Go into module path
    os.chdir(app["path"])

    module = __import__("apps." + app["name"])
    my_class = getattr(module, app["name"])
    my_class.main()

    # Go back to root folder
    os.chdir("/")

def has_intro_played():
    return microcontroller.nvm[NVM_INDEX_INTRO_PLAYED] == 1

def set_intro_played():
    microcontroller.nvm[NVM_INDEX_INTRO_PLAYED] = 1

def is_app_installed(app_name):
    return app_name in os.listdir("/apps")

def get_apps_list():
    apps_items = os.listdir("/apps")
    apps_list = []

    for item in sorted(apps_items):
        if item in ignored_items:
            continue

        path = "/apps/" + item
        stat = os.stat(path)

        if stat[0] & 0x4000:
            apps_list.append({
                "name": item,
                "path": path
            })

    return apps_list

def delete_folder_recursive(path):
    for file in os.listdir(path):
        current_path = path + "/" + file

        stat = os.stat(current_path)
        if stat[0] & 0x4000:
            delete_folder_recursive(current_path)
        else:
            os.remove(current_path)
    os.rmdir(path)

def run_and_display(args):
    if "display_before" in args:
        board.DISPLAY.show(args["display_before"])

    for i, action in enumerate(args["actions"]):
        action(args["actions_args"][i])

    if "display_after" in args:
        board.DISPLAY.show(args["display_after"])

def run_list(args):
    for i, item in enumerate(args["run_actions"]):
        item(args["run_args"][i])

def screensaver():
    io_expander = IOExpander(board.I2C())
    
    display = board.DISPLAY

    # Load the sprite sheet (bitmap)
    niels, niels_p = adafruit_imageload.load("img/niels.bmp",
        bitmap=displayio.Bitmap,
        palette=displayio.Palette)

    niels_p.make_transparent(0)

    # Create a sprite (tilegrid)
    sprite = displayio.TileGrid(niels, pixel_shader=niels_p)

    # Create a Group to hold the sprite
    group = displayio.Group()

    # Add the sprite to the Group
    group.append(sprite)

    # Add the Group to the Display
    display.show(group)

    # Set sprite location
    group.x = random.randint(0, display.width - niels.width)
    group.y = random.randint(0, display.height - niels.height)

    x_speed = 1
    y_speed = 1

    while True:
        # Because of potential delays x2
        io_expander.update()

        if io_expander.any_button_fell:
            return
        
        group.x += x_speed
        group.y += y_speed

        # Because of potential delays x2
        io_expander.update()

        if io_expander.any_button_fell:
            return

        if (group.x + niels.width >= display.width) or (group.x <= 0):
            x_speed = -x_speed
        if (group.y + niels.height >= display.height) or (group.y <= 0):
            y_speed = -y_speed