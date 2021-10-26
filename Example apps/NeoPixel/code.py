"""CircuitPython Essentials NeoPixel example"""
import board
import neopixel
from io_expander import IOExpander

io_expander = IOExpander(board.I2C())
pixel_pin = board.NEOPIXEL
num_pixels = 7

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
def main():
    pixels.fill((255, 0, 0))
    pixels.show()
    io_expander.update()
    while True:
        if io_expander.button_menu.fell:
            return
