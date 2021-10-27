import board
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import settings
import terminalio
from io_expander import IOExpander


colors = [0xFF0000, 0xFFA200, 0xAE00FF, 0x00AF0F, 0xFFFFFF, 0xFFC0CB]

#initialize buttons
io_expander = IOExpander(board.I2C())

display = board.DISPLAY
group = displayio.Group()
font = bitmap_font.load_font("/fonts/spacefont-front-32.pcf")
font.load_glyphs(b'012345QWERTYUIOPLKJHGFDSAZXCVBNM')
whoami_label = label.Label(terminalio.FONT, text="cow@deloitte:~/OOO/2021/CyberCows$ whoami", color=0xFFFFFF)
whoami_label.anchor_point = (0.5, 0.0)
whoami_label.anchored_position = (130, 10)
name_label = label.Label(font, text=settings.cow_name(), color=0xFFFFFF)
name_label.anchor_point = (0.5, 0.5)
name_label.anchored_position = (320 / 2, 240 / 2)
display.show(group)

#group.pop()
group.append(whoami_label)
group.append(name_label)

def main():
    i=0

    while True:
        io_expander.update()
        if io_expander.button_center.fell or io_expander.button_a.fell:
            name_label.color = colors[i]
            i = i +1
            i = i % (len(colors))
        if io_expander.button_menu.fell:
            return
