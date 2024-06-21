import os, json, zipfile ,shutil , subprocess
import toml
import argparse
import rich
from rich.console import Console
from configuration import *
console = Console()


# exc_handler("option", f"message")
def exc_handler(message_type, message):
    if message_type == "error":
        console.print(f":thumbs_down:[{ERROR_COLOR}] log [/{ERROR_COLOR}][{ERR_SUCC_COLOR}]{message}[/{ERR_SUCC_COLOR}]")
    elif message_type == "success":
        console.print(f":thumbs_up:[{SUCCESS_COLOR}] log [/{SUCCESS_COLOR}][{ERR_SUCC_COLOR}]{message}[/{ERR_SUCC_COLOR}]")
    else:
        print(message)  # Default print without any color

def open_paths(path_type):
    if path_type == 'settings':
        if os.path.exists(settings_path):
           
            subprocess.Popen(['explorer', '/open,', settings_path])
            exc_handler("success", f"Opened settings path at {settings_path}")
        else:
            exc_handler("error", f"Settings file not found at {settings_path}")
    elif path_type == 'config':
        if os.path.exists(SERVER_CONFIG):
            subprocess.Popen(['explorer', '/open,', SERVER_CONFIG])
            exc_handler("success", f"Opened config path at {SERVER_CONFIG}")
        else:
            exc_handler("error", f"Config file not found at {SERVER_CONFIG}")
    elif path_type == 'script':
        if os.path.exists(executable_path):
            subprocess.Popen(['explorer', '/open,', executable_path])
            exc_handler("success", f"Opened script path at {executable_path}")
        else:
            exc_handler("error", f"Script file not found at {executable_path}")
    elif path_type == 'maps':
        if os.path.exists(ADDED_MAPS):
            subprocess.Popen(['explorer', '/open,', ADDED_MAPS])
            exc_handler("success", f"Opened maps path at {ADDED_MAPS}")
        else:
            exc_handler("error", f"Maps path not found at {ADDED_MAPS}")
    else: 
        exc_handler("error", f"Please provide the option to open (choose from: 'settings', 'config', 'maps' or 'script')")
def run_execs(option):
    if option == 'tunnel':
        if os.path.exists(TUNNEL_EXE):
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', TUNNEL_EXE])
            #subprocess.run([TUNNEL_EXE], check=True)
            exc_handler("success", f"Tunnel started.")
        else:
            exc_handler("error", f"Tunnel executable not found at {TUNNEL_EXE}")
    elif option == 'server':
        if os.path.exists(SERVER_SHORTCUT):
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', SERVER_SHORTCUT])
            #os.startfile(SERVER_SHORTCUT)
            exc_handler("success", f"Server started.")
        else:
            exc_handler("error", f"Server shortcut not found at {SERVER_SHORTCUT}")
    elif option == 'launcher':
        if os.path.exists(LAUNCHER_SHORTCUT):
            subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', LAUNCHER_SHORTCUT])
            #os.startfile(LAUNCHER_SHORTCUT)
            exc_handler("success", f"Launcher started.")
        else:
            exc_handler("error", f"Launcher shortcut not found at {LAUNCHER_SHORTCUT}")
    else:
        exc_handler("error", f"Please provide the option to run (choose from: 'launcher', 'tunnel' or 'server')")
def sync_maps():
    maps = {}
    map_id = 1

    def process_maps(path, is_default):
        nonlocal map_id
        for file_name in os.listdir(path):
            if file_name.endswith('.zip'):
                file_path = os.path.join(path, file_name)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for name in zip_ref.namelist():
                        if name.startswith('levels/') and name.endswith('/info.json'):
                            map_name = name.split('/')[1].lower()
                            maps[str(map_id)] = {'name': map_name, 'default': is_default, 'zip_name': file_name}
                            map_id += 1
                            break

    process_maps(DEFAULT_MAPS_PATH, True)
    process_maps(ADDED_MAPS_PATH, False)

    with open(MAPS_JSON_PATH, 'w') as file:
        json.dump(maps, file, indent=4)
    exc_handler("success", f"Maps synchronized.")
def list_maps():
    if not os.path.exists(MAPS_JSON_PATH) or os.stat(MAPS_JSON_PATH).st_size == 0:
        
        exc_handler("error", f" No maps found. Automatically running 'sync'.")
        sync_maps()
        list_maps()
        return
    with open(SERVER_CONFIG_PATH, 'r') as file:
        config_lines = file.readlines()

    # Extracting the desired values from the server config
    server_config = {}
    for line in config_lines:
        if line.startswith('Name = "'):
            server_config['Name'] = line.split('=')[1].strip().strip('"')
        elif line.startswith('Port ='):
            server_config['Port'] = line.split('=')[1].strip()
        elif line.startswith('Map = "/levels/'):
            map_path = line.split('=')[1].strip().strip('"')
            map_name = map_path.split('/')[2]  # Extract the map name from the path
            server_config['Map'] = map_name
        elif line.startswith('Private = '):
            server_config['Private'] = line.split('=')[1].strip()
        elif line.startswith('MaxCars = '):
            server_config['MaxCars'] = line.split('=')[1].strip()
        elif line.startswith('MaxPlayers = '):
            server_config['MaxPlayers'] = line.split('=')[1].strip()

    # Print the server config values in the first line with different colors
    config_display = []
    for key, value in server_config.items():
        config_display.append(
            f"[{CONFIG_NAME_COLOR}]{key}[/{CONFIG_NAME_COLOR}][{CONFIG_VALUE_COLOR}][/{CONFIG_VALUE_COLOR}][{DEFAULT_TEXT_COLOR}]{CONFIG_VALUE_SEPARATOR}[/{DEFAULT_TEXT_COLOR}][{CONFIG_VALUE_COLOR}]{value}[/{CONFIG_VALUE_COLOR}]"
        )
    config_values = f"{CONFIG_SEPARATOR}".join(config_display)
    console.print(f"[{DEFAULT_TEXT_COLOR}]{config_values}[/{DEFAULT_TEXT_COLOR}]")
    with open(MAPS_JSON_PATH, 'r') as file:
        maps = json.load(file)
    for map_id, map_data in maps.items():
        map_id = int(map_id)  # Convert map_id to int for printing
        map_name = map_data['name']
        zip_name = map_data.get('zip_name', 'unknown')  # Get zip name or default to 'unknown'
        is_default = map_data['default']
        if is_default:
            map_color_code = DEFAULT_MAP_COLOR  # Assign default map color
        else:
            map_color_code = ADDED_MAP_COLOR   # Assign added map color
        console.print(f"[{NUMBER_COLOR}]{map_id}[/{NUMBER_COLOR}][{DEFAULT_TEXT_COLOR}]{FIRST_SEPERATOR}[/{DEFAULT_TEXT_COLOR}][{map_color_code}]{map_name}[/{map_color_code}][{DEFAULT_TEXT_COLOR}]{SECOND_SEPERATOR}[/{DEFAULT_TEXT_COLOR}][{ZIP_NAME_COLOR}]{zip_name}[/{ZIP_NAME_COLOR}]")


def pick_map(map_identifier):
    map_identifier = map_identifier.lower()

    if not os.path.exists(MAPS_JSON_PATH) or os.stat(MAPS_JSON_PATH).st_size == 0:
        
        exc_handler("error", f"No maps found. Please run with 'sync' first.")
        return

    with open(MAPS_JSON_PATH, 'r') as file:
        maps = json.load(file)

    map_name = None

    # Check if the map_identifier is a number or name
    try:
        map_id = int(map_identifier)
        if str(map_id) in maps:
            map_name = maps[str(map_id)]['name']
    except ValueError:
        if map_identifier in [map_data['name'] for map_data in maps.values()]:
            map_name = map_identifier

    if not map_name:

        exc_handler("error", f"Map with ID or name {map_identifier} not found.")
        return

    with open(SERVER_CONFIG_PATH, 'r') as file:
        config_lines = file.readlines()

    new_config_lines = []
    for line in config_lines:
        if line.startswith('Map = '):
            new_config_lines.append(f'Map = "/levels/{map_name}/info.json"\n')
        else:
            new_config_lines.append(line)

    with open(SERVER_CONFIG_PATH, 'w') as file:
        file.writelines(new_config_lines)


    exc_handler("success", f"Map set to {map_name}")
    # Clear the server resources path
    existing_map_files = [f for f in os.listdir(SERVER_RESOURCES_PATH) if f.endswith('.zip')]
    for existing_map in existing_map_files:
        existing_map_path = os.path.join(SERVER_RESOURCES_PATH, existing_map)
        added_map_names = [name.lower() for name in os.listdir(ADDED_MAPS_PATH)]
    
        if existing_map.lower() not in added_map_names:
            os.remove(existing_map_path)
            exc_handler("success", f"Removed existing map {existing_map} from server resources path.")
        else:
            # Move the existing map to added maps path
            shutil.move(existing_map_path, os.path.join(ADDED_MAPS_PATH, existing_map))
            exc_handler("success", f"Moved existing map {existing_map} to added maps path.")
            
    
    # Copy the new map zip file to the server resources path
    for file_name in os.listdir(ADDED_MAPS_PATH):
        if file_name.endswith('.zip'):
            file_path = os.path.join(ADDED_MAPS_PATH, file_name)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                found = False
                for name in zip_ref.namelist():
                    if name.lower().startswith(f'levels/{map_name.lower()}/') and name.lower().endswith('/info.json'):
                        found = True
                        shutil.copy(file_path, SERVER_RESOURCES_PATH)
                        exc_handler("success", f"Copied {file_name} to server resources path.")
                        
                        break
                if found:
                    return
    exc_handler("error", f"Map {map_name} zip file not found in added maps path.")
