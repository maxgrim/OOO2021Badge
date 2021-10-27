import board
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparklepulse import SparklePulse 
from adafruit_led_animation.color import AMBER
import neopixel
import time
from io_expander import IOExpander

def main():
    #Button handler
    io_expander = IOExpander(board.I2C())

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 7, brightness=1.0, auto_write=True)
    comet = Comet(pixels, speed=0.01, color=AMBER, tail_length=10, bounce=True)
    pulse = Pulse(pixels, speed=0.1, color=AMBER, period=3)
    sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=AMBER)
    i=0
    font = bitmap_font.load_font("/fonts/spacefont-front-32.pcf")
    font.load_glyphs(b'012345QWERTYUIOPLKJHGFDSAZXCVBNM')
    animation_label = label.Label(font, text="", color=0xFFFFFF)
    animation_label.anchor_point = (0.5, 0.5)
    animation_label.anchored_position = (320 / 2, 240 / 2)
    display = board.DISPLAY
    group = displayio.Group()
    group.append(animation_label)
    display.show(group)

    while True:
        io_expander.update()
        pixels.fill((0, 0, 0))
        animation_label.text = "PRESS A/B/S"
        if io_expander.button_a.fell:
            for i in range(100):
                comet.animate()
                animation_label.text = "COMET"
            i=0
        if io_expander.button_b.fell:
            for i in range(100):
                pulse.animate()
                animation_label.text = "PULSE"
            i=0
        if io_expander.button_select.fell: 
            for i in range(100):
                sparkle_pulse.animate()
                animation_label.text = "SPARKLE"
            i=0
        if io_expander.button_menu.fell:
                return


            
