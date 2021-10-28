import board
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload
import neopixel
import time
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import AMBER
import settings


def display_rocket():
    display = board.DISPLAY

    # Load the sprite sheet (bitmap)
    rocket, rocket_p = adafruit_imageload.load("8.bmp",
                                                    bitmap=displayio.Bitmap,
                                                    palette=displayio.Palette)
    rocket_p.make_transparent(0)
    # Create a sprite (tilegrid)
    sprite = displayio.TileGrid(rocket, pixel_shader=rocket_p)
    # Create a Group to hold the sprite
    group = displayio.Group()
    # Add the sprite to the Group
    group.append(sprite)
    # Add the Group to the Display
    display.show(group)
    # Set sprite location
    group.x = 160
    group.y = 240
    x_speed = 1
    y_speed = 1

    while True:
        group.y -= 2
        group.y += y_speed
        time.sleep(0.01)

        if group.y == -50:
            return
        
def main():
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 7, brightness=1.0, auto_write=True)
    pulse = Pulse(pixels, speed=0.01, color=AMBER, period=3)

    font = bitmap_font.load_font("/fonts/spacefont-front-32.pcf")
    font.load_glyphs(b'012345QWERTYUIOPLKJHGFDSAZXCVBNM')

    countdown_label = label.Label(font, text="", color=0xFFFFFF)
    countdown_label.anchor_point = (0.5, 0.5)
    countdown_label.anchored_position = (320 / 2, 240 / 2)

    display = board.DISPLAY
    group = displayio.Group()
    group.append(countdown_label)
    display.show(group)

    scow_spacer = 10
    start_y = (240) #- (48 * 3 + (4 * scow_spacer)) - 150

    cowname_label = label.Label(font, text=settings.cow_name(), color=0xFFFFFF)
    cowname_label.anchor_point = (0.5, 0.5)
    cowname_label.anchored_position = (320 / 2, start_y)

    welcome_label = label.Label(font, text="WELCOME", color=0xFFFFFF)
    welcome_label.anchor_point = (0.5, 0.5)
    welcome_label.anchored_position = (320 / 2, start_y)

    to_label = label.Label(font, text="TO", color=0xFFFFFF)
    to_label.anchor_point = (0.5, 0.5)
    to_label.anchored_position = (320 / 2, start_y + scow_spacer + welcome_label.height)

    scows_label = label.Label(font, text="SPACE COWS", color=0xFFFFFF)
    scows_label.anchor_point = (0.5, 0.5)
    scows_label.anchored_position = (320 / 2, start_y + (scow_spacer * 2) + welcome_label.height + to_label.height)

    rocket_label = label.Label(font, text="SPACE COWS", color=0xFFFFFF)
    rocket_label.anchor_point = (0.5, 0.5)
    rocket_label.anchored_position = (320 / 2, start_y + (scow_spacer * 2) + welcome_label.height + to_label.height + scows_label.height)

    for i in range(6):
        countdown_label.text = str(5 - i)
        time.sleep(1)

    group.pop()
    group.append(cowname_label)
    group.append(welcome_label)
    group.append(to_label)
    group.append(scows_label)

    while True:
        pulse.animate()
        cowname_label.anchored_position = (320 / 2, start_y)
        welcome_label.anchored_position = (320 / 2, start_y + scow_spacer + welcome_label.height)
        to_label.anchored_position = (320 / 2, start_y + (scow_spacer * 2) + welcome_label.height + to_label.height)
        scows_label.anchored_position = (320 / 2, start_y + (scow_spacer * 3) + welcome_label.height + to_label.height + scows_label.height)
        start_y -= 2
        time.sleep(0.01)
        
        if start_y == -200:
            display_rocket()
            pixels.deinit()
            return
