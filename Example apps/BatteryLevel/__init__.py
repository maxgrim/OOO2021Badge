"""CircuitPython Essentials Analog In example"""
import time
import board
from analogio import AnalogIn
import adafruit_imageload
import displayio

display = board.DISPLAY
analog_in = AnalogIn(board.SENSE_BATT)

def get_battery_percentage():
    battery_mean_calc = 0
    for x in range(0, 200):
        battery_mean_calc = analog_in.value + battery_mean_calc
        if x == 199:
            battery_mean_calc = int((((battery_mean_calc/200)-34000) * 100)/(41000-34000))
            if battery_mean_calc > 90:
                print("Charging")
                sprite[0] = 0 % 6
            if battery_mean_calc > 66 and battery_mean_calc < 90:
                print("Full")
                sprite[0] = 1 % 6
            if battery_mean_calc > 33 and battery_mean_calc < 66:
                print("Medium")
                sprite[0] = 2 % 6
            if battery_mean_calc > 0 and battery_mean_calc < 33:
                print("Low")
                sprite[0] = 3 % 6
        x = x +1
# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("batteries.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=9,
                            tile_height=4)

# Create a Group to hold the sprite
group = displayio.Group(scale=3)

# Add the sprite to the Group
group.append(sprite)

# Add the Group to the Display
display.show(group)

# Set sprite location
group.x = 290
group.y = 0

# Loop through each sprite in the sprite sheet

while True:
    get_battery_percentage()
