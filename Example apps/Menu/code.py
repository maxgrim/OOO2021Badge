import board
import displayio
import menu
from io_expander import IOExpander
import about
import logo
import appstore


display = board.DISPLAY
d_group_root = displayio.Group()
display.show(d_group_root)

def run_and_display_group(args):
    args["action"](args["action_args"])
    display.show(args["display_group"])

logo_height = logo.display_logo(d_group_root, display.width / 2, 25)

root_menu = menu.Menu(start_y=logo_height + 20)

root_menu.add_entry(menu.MenuLabelEntry("Apps", None, None))
root_menu.add_entry(menu.MenuLabelEntry("Install new apps", run_and_display_group, {
    "action": appstore.run_store,
    "action_args": None,
    "display_group": d_group_root
}))

root_menu.add_entry(menu.MenuLabelEntry("Settings", None, None))
root_menu.add_entry(menu.MenuLabelEntry("About", run_and_display_group, {
    "action": about.show_about,
    "action_args": None,
    "display_group": d_group_root
}))

d_group_root.append(root_menu.display_group)
menu_collection = menu.MenuCollection(root_menu)

io_expander = IOExpander(board.I2C())

while True:
    io_expander.update()

    if io_expander.button_down.fell:
        menu_collection.active_menu.move_down()

    if io_expander.button_up.fell:
        menu_collection.active_menu.move_up()

    # Think about support for the settings menu (different type of action)
    if io_expander.button_center.fell or io_expander.button_a.fell:
        selected_item = menu_collection.active_menu.selected_item
        selected_item.execute_action()