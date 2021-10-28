from adafruit_display_text import label, wrap_text_to_pixels
import terminalio
import displayio
import board


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
        if len(self.menu_stack) > 1:
            last_menu = self.menu_stack.pop()
            del self.menus[last_menu]

class Menu:
    def __init__(self, start_x=10, start_y=10):
        self.entries = []
        self.display_group = displayio.Group()
        self.display_menu_group = displayio.Group()
        self.display_activity_i_group = displayio.Group()

        self.start_x = start_x
        self.start_y = start_y

        self.active_index = 0
        self.active_indicator = label.Label(terminalio.FONT, \
            text=">", color=0xFF0000)
        self.active_indicator.anchor_point = (0.0, 0.5)

        self.display_activity_i_group.append(self.active_indicator)
        self.display_group.append(self.display_activity_i_group)
        self.display_group.append(self.display_menu_group)

    def add_entry(self, entry):
        # Correct placement
        entry.label.anchor_point = (0.0, 0.0)
        entry.label.anchored_position = \
            (20, self.start_y + self.active_indicator.height * len(self.entries))
        
        self.entries.append(entry)
        self.display_menu_group.append(entry.label)

        if len(self.entries) == 1:
            self.update_active_indicator()

    def move_up(self):
        if len(self.entries) == 0:
            return

        if self.active_index - 1 < 0:
            return

        self.active_index = self.active_index - 1

        if self.active_indicator.y < self.active_indicator.height:
            self.display_menu_group.y = self.display_menu_group.y + self.active_indicator.height

        self.update_active_indicator()

    def move_down(self):
        if len(self.entries) == 0:
            return

        if self.active_index + 1 >= len(self.entries):
            return

        self.active_index = self.active_index + 1

        if self.active_indicator.y > board.DISPLAY.height - self.active_indicator.height:
            self.display_menu_group.y = self.display_menu_group.y - self.active_indicator.height
        
        self.update_active_indicator()

    def update_active_indicator(self):
        self.active_indicator.anchored_position = \
            (5, self.entries[self.active_index].label.y + self.display_menu_group.y)

    @property
    def selected_item(self):
        return self.entries[self.active_index]