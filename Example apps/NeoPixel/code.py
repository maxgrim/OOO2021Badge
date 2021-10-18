"""CircuitPython Essentials NeoPixel example"""
import board
import neopixel

pixel_pin = board.NEOPIXEL
num_pixels = 7

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

pixels.fill((255, 0, 0))
pixels.show()