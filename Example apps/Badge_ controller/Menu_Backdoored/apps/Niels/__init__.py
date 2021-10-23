import time
import board
import displayio
import adafruit_imageload
import random

from tca9539 import TCA9539
from adafruit_debouncer import Debouncer


def main():
    io_expander = TCA9539(board.I2C())
    b_button = Debouncer(io_expander.get_pin(15))

    display = board.DISPLAY
    # display.brightness = 1.0

    # Load the sprite sheet (bitmap)
    niels, niels_p = adafruit_imageload.load("niels.bmp",
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
    group.x = random.randint(0, 320 - niels.width)
    group.y = random.randint(0, 240 - niels.height)

    width = 320
    height = 240

    x_speed = 1
    y_speed = 1

    while True:
        io_expander.gpio_update()
        b_button.update()

        if b_button.fell:
            return

        if (group.x + niels.width >= width) or (group.x <= 0):
            x_speed = -x_speed
        if (group.y + niels.height >= height) or (group.y <= 0):
            y_speed = -y_speed
        group.x += x_speed
        group.y += y_speed
        time.sleep(0.01)
