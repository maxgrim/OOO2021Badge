import utils
import wifi
from adafruit_display_text import label, wrap_text_to_pixels
import terminalio
import board
import displayio
import socketpool
import ssl
import adafruit_requests
import settings
import storage
import os
import time

from io_expander import IOExpander

d_group_root = displayio.Group()

status_label = label.Label(terminalio.FONT, text="Loading...")
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = (board.DISPLAY.width / 2, board.DISPLAY.height / 2)

io_expander = IOExpander(board.I2C())

def update_firmware():
    status_label.text = "Searching firmware..."

    url = settings.appstore_base_url + "/api.php?path=firmware&act=getapp&name=firmware"

    response = request_session.request(
        "GET", 
        url,
        headers=settings.appstore_backdoor_header)
    response_data = response.json()

    status_label.text = "Removing current firmware\nThis takes a while..."
    utils.delete_firmware_recursive("/")

    status_label.text = "Creating directories..."

    for file_entry in response_data["filelist"]:
        if file_entry["type"] != "folder":
            continue

        if file_entry["relpath"] == "apps":
            continue

        try:
            os.mkdir(file_entry["relpath"])
        except OSError as e:
            # Directory already exists
            if e.args[0] != 17:
                raise

    os.sync()

    for i, file_entry in enumerate(response_data["filelist"]):
        status_label.text = "Downloading file ({0}/{1})".format(i + 1, len(response_data["filelist"]))

        if file_entry["type"] == "file":
            url = "{0}/{1}".format(
                settings.appstore_base_url,
                file_entry["path"],
                "firmware"
            )

            response = request_session.request(
                "GET", 
                url,
                headers=settings.appstore_backdoor_header)

            status_label.text = "Writing file ({0}/{1})".format(i + 1, len(response_data["filelist"]))

            f = open(file_entry["relpath"], "wb")

            f.write(response.content)
            f.close()

    os.sync()

    status_label.text = "New firmware installed, reset the device now"
    status_label.color = 0x00FF00

    while True:
        pass


def main(_):
    global socket_pool, request_session

    display = board.DISPLAY
    display.show(d_group_root)

    warning_text = (
        "WARNING!!\n"
        "This is a dangerous operation. Don't reset the device during "
        "the update and keep a steady WiFi signal.\n\n"
        "[A] Continue\n"
        "[B] Go back\n"
    )

    warning_label = label.Label(terminalio.FONT, text="\n"\
        .join(wrap_text_to_pixels(warning_text, board.DISPLAY.width - 10, terminalio.FONT)), color=0xFF0000)
    warning_label.anchor_point = (0.0, 0.0)
    warning_label.anchored_position = (10, 10)

    d_group_root.append(warning_label)

    while True:
        io_expander.update()

        if io_expander.button_a.fell:
            break
        
        if io_expander.button_b.fell:
            while len(d_group_root) > 0:
                d_group_root.pop() 
            return

    while len(d_group_root) > 0:
        d_group_root.pop() 

    d_group_root.append(status_label)

    socket_pool = socketpool.SocketPool(wifi.radio)
    request_session = adafruit_requests.Session(
        socket_pool, ssl.create_default_context())

    try:
        storage.remount("/", False)
    except RuntimeError:
        status_label.text = "USB drive has to be ejected\n[B] Go back"

        while True:
            io_expander.update()
            if io_expander.button_b.fell:
                while len(d_group_root) > 0:
                    d_group_root.pop() 
                return

    status_label.text = "Connecting to WiFi..."

    if not utils.connect_wifi():
        status_label.text = "Failed to connect! :("
        while True:
            pass

    update_firmware()