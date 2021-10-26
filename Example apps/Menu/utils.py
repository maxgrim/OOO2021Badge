import os
import board


ignored_items = [".DS_Store", "._.DS_Store"]

def start_app(args):
    app = args["app"]
    # Go into module path
    os.chdir(app["path"])

    module = __import__("apps." + app["name"])
    my_class = getattr(module, app["name"])
    my_class.main()

    # Go back to root folder
    os.chdir("/")

# TODO: read manifest for title etc
def get_apps_list():
    apps_items = os.listdir("/apps")
    apps_list = []

    for item in sorted(apps_items):
        if item in ignored_items:
            continue

        path = "/apps/" + item
        stat = os.stat(path)

        if stat[0] & 0x4000:
            apps_list.append({
                "name": item,
                "path": path
            })

    return apps_list

def delete_folder_recursive(path):
    for file in os.listdir(path):
        current_path = path + "/" + file

        stat = os.stat(current_path)
        if stat[0] & 0x4000:
            delete_folder_recursive(current_path)
        else:
            os.remove(current_path)
    os.rmdir(path)

def run_then_display_show(args):
    args["action"](args["action_args"])
    board.DISPLAY.show(args["display_group"])
