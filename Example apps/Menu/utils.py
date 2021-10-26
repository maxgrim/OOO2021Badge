import os

ignored_items = [".DS_Store", "._.DS_Store"]

def start_app(args):
    # Go into module path
    os.chdir(args[2])

    module = __import__("apps." + args[1])
    my_class = getattr(module, args[1])
    my_class.main()

    # Go back to root folder
    os.chdir("/")
    
    # Call callback function
    return args[0](None)

def get_apps_list(end_callback):
    apps_items = os.listdir("/apps")
    apps_list = []

    for item in sorted(apps_items):
        if item in ignored_items:
            continue

        path = "/apps/" + item
        stat = os.stat(path)

        if stat[0] & 0x4000:
            apps_list.append({
                "text": item, 
                "action": start_app,
                "args": [end_callback, item, path]
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
