from font import space_font_back, space_font_front
from adafruit_display_text import label


def display_logo(group, x, y):
    space_label = label.Label(space_font_back, text="SPACE", color=0xFFFFFF)
    space_label.anchor_point = (0.5, 0.5)
    space_label.anchored_position = (x, y)
    group.append(space_label)    
    cows_label = label.Label(space_font_front, text="COWS", color=0xFFFFFF)
    cows_label.anchor_point = (0.5, 0.5)
    cows_label.anchored_position = (x, y + space_label.height * 0.9)
    group.append(cows_label)
    return space_label.height + space_label.height * 0.9