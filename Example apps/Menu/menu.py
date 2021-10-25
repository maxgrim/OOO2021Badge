from adafruit_display_text import label, wrap_text_to_pixels
from adafruit_bitmap_font import bitmap_font
import terminalio
import displayio


class Menu:
    def __init__(self, heading=None):
        self.items = []
        self.display_group = displayio.Group()

        self.start_y = 0

        if heading is not None:
            heading_label = label.Label(
                terminalio.FONT,
                text="\n".join(wrap_text_to_pixels(
                    heading, 300, terminalio.FONT))
                )
            
            heading_label.anchor_point = (0.0, 0.0)
            heading_label.anchored_position = (20, 20)

            self.display_group.append(heading_label)
            self.start_y = self.start_y + \
                heading_label.y + heading_label.height

        self.active_index = 0
        self.active_label = label.Label(terminalio.FONT, \
            text=">", color=0xFF0000)
        self.active_label.anchor_point = (0.0, 0.0)
        self.display_group.append(self.active_label)

        self.update_active_label()
        
    def update_active_label(self):
        self.active_label.anchored_position = \
            (5, self.start_y + self.active_index * 21)

    def add_label(self, text, action, action_args):
        menu_label = label.Label(terminalio.FONT, \
            text=text, color=0xFFFFFF)
        menu_label.anchor_point = (0.0, 0.0)
        menu_label.anchored_position = \
            (20, self.start_y + 21 * len(self.items))

        self.items.append({
            "text": text,
            "action": action,
            "action_args": action_args,
            "label": menu_label
        })

        self.display_group.append(menu_label)

    def menu_up(self):
        self.active_index = self.active_index - 1
        self.active_index %= len(self.items)
        self.update_active_label()

    def menu_down(self):
        self.active_index = self.active_index + 1
        self.active_index %= len(self.items)
        self.update_active_label()

    def menu_select(self):
        return self.items[self.active_index]