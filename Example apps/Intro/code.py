import board
import displayio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

import neopixel

import time

pixels = neopixel.NeoPixel(board.NEOPIXEL, 7, brightness=0.0, auto_write=True)
pixels.fill((225, 180, 0))

font = bitmap_font.load_font("fonts/spacecows-32.pcf")
font.load_glyphs(b'012345WELCOMETOSPACECOWS')

countdown_label = label.Label(font, text="", color=0xFFFFFF)
countdown_label.anchor_point = (0.5, 0.5)
countdown_label.anchored_position = (320 / 2, 240 / 2)

display = board.DISPLAY
group = displayio.Group()
group.append(countdown_label)
display.show(group)

scow_spacer = 10
start_y = (240) - (48 * 3 + (4 * scow_spacer)) - 150

welcome_label = label.Label(font, text="WELCOME", color=0xFFFFFF)
welcome_label.anchor_point = (0.5, 0.5)
welcome_label.anchored_position = (320 / 2, start_y)

to_label = label.Label(font, text="TO", color=0xFFFFFF)
to_label.anchor_point = (0.5, 0.5)
to_label.anchored_position = (320 / 2, start_y + scow_spacer + welcome_label.height)

scows_label = label.Label(font, text="SPACE COWS", color=0xFFFFFF)
scows_label.anchor_point = (0.5, 0.5)
scows_label.anchored_position = (320 / 2, start_y + (scow_spacer * 2) + welcome_label.height + to_label.height)

for i in range(6):
    pixels.brightness = 0.1 * i
    countdown_label.text = str(5 - i)
    time.sleep(1)

group.pop()
group.append(welcome_label)
group.append(to_label)
group.append(scows_label)

while True:
    welcome_label.anchored_position = (320 / 2, start_y)
    to_label.anchored_position = (320 / 2, start_y + scow_spacer + welcome_label.height)
    scows_label.anchored_position = (320 / 2, start_y + (scow_spacer * 2) + welcome_label.height + to_label.height)

    start_y += 2
    time.sleep(0.01)