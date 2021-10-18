from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import terminalio

class Menu:
    def __init__(self, items):
        self.active_item = 0
        self.items = items

    def initialize_labels(self, start_x, start_y):
        self.labels = []

        # font = bitmap_font.load_font("/font/Consolas-14.pcf")
        font = terminalio.FONT
        # font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890>')

        for i, item in enumerate(self.items):
            if i == 0:
                item["text"] = "> " + item["text"]
            
            menu_label = label.Label(font, text=item["text"], color=0x0000FF)
            menu_label.anchor_point = (0.0, 0.0)
            menu_label.anchored_position = (start_x, start_y + (21 * i))

            self.labels.append(menu_label)
    
    # direction 0 DOWN, 1 UP
    def menu_move(self, direction):
        self.labels[self.active_item].text = \
            self.labels[self.active_item].text[2:]
        
        self.active_item += (1 if not direction else -1)
        self.active_item %= len(self.items)

        self.labels[self.active_item].text = \
            "> " + self.labels[self.active_item].text

    def get_active_item(self):
        return self.items[self.active_item]