import board
import displayio
import menu
import logo
import os
import supervisor
import pulseio
import adafruit_irremote
from tca9539 import TCA9539
from adafruit_debouncer import Debouncer

supervisor.disable_autoreload()

ignored_items = [".DS_Store", "._.DS_Store"]

# IR backdoor
IR_PIN = board.IR_RECV # Pin connected to IR receiver.

# Expected pulse, pasted in from previous recording REPL session:
#pulse = [8994, 4485, 549, 594, 546, 591, 549, 591, 549, 591, 549, 591, 549, 591, 549, 591, 546, 594, 546, 1716, 546, 1713, 549, 1713, 549, 1713, 552, 1710, 549, 1713, 570, 1692, 573, 570, 546, 1716, 570, 1692, 549, 594, 546, 1713, 549, 1713, 549, 591, 570, 570, 570, 570, 549, 591, 549, 591, 546, 1713, 549, 594, 567, 570, 549, 1713, 570, 1692, 549, 1713, 549]
IR_a_RCV = [9525, 4473, 573, 531, 576, 513, 564, 540, 558, 546, 555, 546, 531, 573, 549, 555, 549, 555, 573, 1671, 561, 1695, 549, 1713, 549, 1689, 534, 1728, 573, 1671, 558, 546, 552, 1704, 549, 558, 573, 531, 570, 519, 558, 543, 558, 546, 531, 570, 573, 531, 573, 534, 549, 1692, 561, 1695, 573, 1689, 573, 1668, 534, 1725, 576, 1671, 558, 1695, 573]
IR_b_RCV = [9528, 4470, 579, 528, 549, 555, 576, 528, 579, 528, 552, 534, 534, 570, 531, 573, 531, 570, 486, 1773, 555, 1689, 531, 1725, 555, 1689, 537, 1719, 579, 1683, 576, 534, 540, 1695, 519, 585, 579, 1683, 576, 510, 537, 567, 531, 573, 483, 621, 519, 582, 552, 555, 552, 1689, 537, 567, 531, 1728, 579, 1662, 564, 1695, 552, 1710, 576, 1665, 531]
#IR_left_RCV = [9483, 4515, 531, 573, 483, 621, 519, 582, 552, 555, 552, 552, 552, 555, 576, 510, 537, 564, 534, 1725, 576, 1686, 549, 1692, 531, 1728, 576, 1665, 531, 1728, 552, 552, 579, 1665, 531, 1725, 552, 552, 552, 555, 576, 1665, 531, 1725, 552, 555, 576, 1665, 534, 573, 480, 1776, 552, 552, 576, 1668, 531, 1725, 552, 1689, 540, 1719, 552, 1710, 552]
#IR_right_RCV = [9510, 4491, 558, 546, 555, 546, 573, 531, 576, 531, 573, 531, 573, 534, 573, 513, 585, 519, 558, 1695, 576, 1671, 588, 1668, 534, 1725, 576, 1668, 558, 1698, 576, 531, 573, 1671, 558, 1695, 576, 1671, 588, 519, 558, 543, 558, 1698, 576, 1671, 582, 522, 558, 546, 555, 1701, 573, 531, 576, 1665, 558, 1701, 573, 1674, 582, 1671, 573, 1689, 576]
IR_up_RCV = [9510, 4491, 558, 546, 573, 531, 573, 534, 573, 531, 573, 531, 573, 534, 540, 546, 555, 546, 558, 1701, 573, 1671, 558, 1695, 576, 1671, 588, 1668, 555, 1707, 573, 531, 573, 1668, 558, 1701, 573, 1671, 558, 1698, 573, 531, 573, 1674, 558, 546, 555, 1698, 576, 531, 573, 1671, 558, 546, 555, 1698, 576, 1671, 558, 1695, 576, 1689, 573, 1665, 558]
IR_down_RCV = [9513, 4491, 558, 546, 555, 546, 558, 546, 570, 531, 576, 531, 573, 531, 573, 534, 573, 516, 558, 1692, 576, 1686, 576, 1665, 561, 1698, 576, 1671, 558, 1695, 576, 531, 573, 1671, 561, 1692, 576, 1686, 576, 1665, 561, 1698, 576, 1671, 558, 1695, 576, 1686, 576, 516, 558, 1692, 576, 531, 573, 1674, 585, 1668, 573, 1686, 576, 1668, 558, 1698, 576]
IR_menu_RCV = [9525, 4473, 576, 531, 573, 9525, 582, 519, 558, 543, 558, 546, 558, 543, 576, 531, 573, 534, 570, 1671, 558, 1695, 576, 1686, 576, 1665, 561, 1698, 576, 1668, 561, 546, 555, 1698, 576, 534, 573, 1668, 558, 1698, 576, 531, 573, 1668, 558, 546, 558, 570, 546, 558, 546, 1689, 573, 519, 555, 1695, 576, 1686, 576, 1665, 561, 1698, 576, 1668, 561]
def fuzzy_pulse_compare(pulse1, pulse2, fuzzyness=0.2):
    if len(pulse1) != len(pulse2):
        return False
    for i in range(len(pulse1)):
        threshold = int(pulse1[i] * fuzzyness)
        if abs(pulse1[i] - pulse2[i]) > threshold:
            return False
    return True

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()
pulses.clear()
pulses.resume()


def start_app(args):
    # Go into module path
    os.chdir(args[1])

    module = __import__("apps." + args[0])
    my_class = getattr(module, args[0])
    my_class.main()

    # Go back to root folder
    os.chdir("/")
    
    return go_to_main_menu(None)

def get_apps_list():
    apps_items = os.listdir("/apps")
    apps_list = []

    for item in sorted(apps_items):
        if item in ignored_items:
            continue

        path = "/apps/" + item
        stat = os.stat(path)

        if stat[0] & 0x4000:
            # Directory
            # TODO: Read manifest
            # - Title
            # - BMP icon
            # - Category (?)
            # - Author
            # - Description

            apps_list.append({
                "text": item, 
                "action": start_app,
                "args": [item, path]
            })

    return apps_list

display = board.DISPLAY
group = displayio.Group()
display.show(group)

logo_tuple = logo.load_logo()
logo.display_logo(group, logo_tuple, 
    int(board.DISPLAY.width / 2 - (logo_tuple[0].width / 2)), 10)

main_menu_group = displayio.Group()
app_menu_group = displayio.Group()

def go_to_app_menu(args):
    group.pop()
    group.append(app_menu_group)
    return 1

def go_to_main_menu(args):
    group.pop()
    group.append(main_menu_group)
    display.show(group)
    return 0

app_menu_items = get_apps_list()

main_menu_items = [
    {"text": "Apps", "action": go_to_app_menu, "args": None},
    {"text": "Install new apps", "action": go_to_app_menu, "args": None},
    {"text": "Settings", "action": go_to_app_menu, "args": None},
    {"text": "Check for updates", "action": go_to_app_menu, "args": None},
    {"text": "About", "action": go_to_app_menu, "args": None},
    {"text": "Deep sleep", "action": go_to_app_menu, "args": None}
]

app_menu = menu.Menu(app_menu_items)
app_menu.initialize_labels(20, logo_tuple[0].height + 20)

for label in app_menu.labels:
    app_menu_group.append(label)

main_menu = menu.Menu(main_menu_items)
main_menu.initialize_labels(20, logo_tuple[0].height + 20)

for label in main_menu.labels:
    main_menu_group.append(label)

group.append(main_menu_group)

menus = [main_menu, app_menu]
current_menu = 0

io_expander = TCA9539(board.I2C())
down_button = Debouncer(io_expander.get_pin(9))
up_button = Debouncer(io_expander.get_pin(12))
center_button = Debouncer(io_expander.get_pin(10))
a_button = Debouncer(io_expander.get_pin(4))

while True:
    io_expander.gpio_update()
    down_button.update()
    up_button.update()
    center_button.update()
    a_button.update()
    detected = decoder.read_pulses(pulses)
    if down_button.fell or fuzzy_pulse_compare(IR_down_RCV, detected):
        menus[current_menu].menu_move(0)

    if up_button.fell or fuzzy_pulse_compare(IR_up_RCV, detected):
        menus[current_menu].menu_move(1)

    if center_button.fell or a_button.fell or fuzzy_pulse_compare(IR_a_RCV, detected):
        active_item = menus[current_menu].get_active_item()
        action = active_item["action"]
        current_menu = action(active_item["args"])