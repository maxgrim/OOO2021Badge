import time
import board
import displayio
import adafruit_imageload
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer

display = board.DISPLAY

#Button handler
io_expander = TCA9539(board.I2C())
menu_button = Debouncer(io_expander.get_pin(15))

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("apps/Parrot/bmps/led_matrices_parrot-vertical.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=32,
                            tile_height=32)

# Create a Group to hold the sprite
group = displayio.Group(scale=3)

# Add the sprite to the Group
group.append(sprite)

# Add the Group to the Display
display.show(group)

# Set sprite location
group.x = 120
group.y = 60

# Loop through each sprite in the sprite sheet
source_index = 0
def main():
    while True:
        io_expander.gpio_update()
        menu_button.update()
        sprite[0] = source_index % 6
        source_index += 1
        time.sleep(0.075)
        if menu_button.fell:
            return