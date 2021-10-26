from adafruit_display_text import label, wrap_text_to_pixels
from adafruit_bitmap_font import bitmap_font
import terminalio
import displayio


class MenuCheckboxEntry:
    def __init__(self, text):
        pass


class MenuLabelEntry:
    def __init__(self, text, action, action_args_dict):
        self.text = text
        self.action = action
        self.action_args_dict = action_args_dict

        self.label = label.Label(terminalio.FONT, \
            text=text, color=0xFFFFFF)

    def execute_action(self):
        self.action(self.action_args_dict)


class MenuCollection:
    def __init__(self, root_menu):
        self.menu_stack = ["root"]
        self.menus = {
            "root": root_menu
        }
    
    @property
    def active_menu(self):
        return self.menus[self.menu_stack[-1]]
    
    def push_menu(self, menu, menu_name):
        self.menus[menu_name] = menu
        self.menu_stack.append(menu_name)

    def pop_menu(self):
        last_menu = self.menu_stack.pop()
        del self.menus[last_menu]

class Menu:
    def __init__(self, start_x=10, start_y=10, heading=None):
        self.entries = []
        self.display_group = displayio.Group()

        self.start_x = start_x
        self.start_y = start_y

        if heading is not None:
            heading_label = label.Label(
                terminalio.FONT,
                text="\n".join(wrap_text_to_pixels(
                    heading, 300, terminalio.FONT)),
                color=0x00FF00
            )
            
            heading_label.anchor_point = (0.0, 0.0)
            heading_label.anchored_position = \
                (self.start_x, self.start_y)

            self.display_group.append(heading_label)
            self.start_y = self.start_y + \
                heading_label.y + heading_label.height

        self.active_index = 0
        self.active_indicator = label.Label(terminalio.FONT, \
            text=">", color=0xFF0000)
        self.active_indicator.anchor_point = (0.0, 0.0)
        self.display_group.append(self.active_indicator)

        self.update_active_indicator()

    def add_entry(self, entry):
        # Correct placement
        entry.label.anchor_point = (0.0, 0.0)
        entry.label.anchored_position = \
            (20, self.start_y + 21 * len(self.entries))
        
        self.entries.append(entry)
        self.display_group.append(entry.label)

    def move_up(self):
        self.active_index = self.active_index - 1
        self.active_index %= len(self.entries)
        self.update_active_indicator()

    def move_down(self):
        self.active_index = self.active_index + 1
        self.active_index %= len(self.entries)
        self.update_active_indicator()

    def update_active_indicator(self):
        self.active_indicator.anchored_position = \
            (5, self.start_y + self.active_index * 21)

    @property
    def selected_item(self):
        return self.entries[self.active_index]