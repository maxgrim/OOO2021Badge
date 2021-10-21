import time
import board
import displayio
import adafruit_imageload

display = board.DISPLAY

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("bmps/led_matrices_parrot-vertical.bmp",
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
while True:
    sprite[0] = source_index % 6
    source_index += 1
    time.sleep(0.075)
