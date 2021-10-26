
import time
import board
import adafruit_pcf8563
import displayio
from io_expander import IOExpander
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

io_expander = IOExpander(board.I2C())
i2c_bus = board.I2C()
rtc = adafruit_pcf8563.PCF8563(i2c_bus)

days = ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY")

# Set date / time
t = time.struct_time((2021, 10, 21, 21, 38, 0, 1, -1, -1))
rtc.datetime = t
font = bitmap_font.load_font("spacecows-32.pcf")
font.load_glyphs(b'012345NDAYSRITOUMWEHF')
time_spacer = 10
start_y = (240) - (120 + (6*time_spacer))
def main():
    while True:
        io_expander.update()
        if rtc.datetime_compromised:
            print("RTC unset")
            time.sleep(1)  # wait a second
            continue
        else:
            print("RTC reports time is valid")
        t = rtc.datetime
        time_label = label.Label(font, text="{}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec), color=0xFFFFFF)
        time_label.anchor_point = (0.5, 0.5)
        time_label.anchored_position = (320 / 2, start_y)
        date_label = label.Label(font, text="{}/{}/{}".format(t.tm_mday, t.tm_mon, t.tm_year), color=0xFFFFFF)
        date_label.anchor_point = (0.5, 0.5)
        date_label.anchored_position = (320 / 2, start_y + time_spacer + time_label.height)
        day_label = label.Label(font, text="{}".format(days[int(t.tm_wday)]), color=0xFFFFFF)
        day_label.anchor_point = (0.5, 0.5)
        day_label.anchored_position = (320 / 2, start_y + 2*time_spacer + time_label.height + date_label.height)
        display = board.DISPLAY
        group = displayio.Group()
        group.append(date_label)
        display.show(group)
        group.pop()
        group.append(time_label)
        group.append(date_label)
        group.append(day_label)
        time.sleep(1)  # wait a secondimport board
        if io_expander.button_menu.fell:
            return

