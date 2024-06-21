import sys, toml, os
# Determine the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Determine the directory of the executable or script
executable_path = os.path.abspath(sys.argv[0])
script_directory = os.path.dirname(executable_path)

# Construct path to settings.toml relative to script_directory
settings_path = os.path.join(script_directory, 'settings.toml')
with open(settings_path, 'r') as file:
    settings = toml.load(file)


# Path configurations
DEFAULT_MAPS_PATH = settings['paths']['default_maps_path']
ADDED_MAPS_PATH = settings['paths']['added_maps_path']
SERVER_CONFIG_PATH = settings['paths']['server_config_path']
SERVER_RESOURCES_PATH = settings['paths']['server_resources_path']
MAPS_JSON_PATH = os.path.join(script_dir, 'maps.json')

# other configuration settings
FIRST_SEPERATOR = settings['other']['first_separator']
SECOND_SEPERATOR = settings['other']['second_separator']
CONFIG_SEPARATOR = settings['other']['config_separator']
CONFIG_VALUE_SEPARATOR = settings['other']['config_value_separator']

ADDED_MAPS = os.path.normpath(settings['paths']['added_maps_path'])
SERVER_CONFIG = os.path.normpath(settings['paths']['server_config_path'])
SERVER_SHORTCUT = os.path.normpath(settings['paths']['server_shortcut_path'])
TUNNEL_EXE = os.path.normpath(settings['paths']['tunnel_exe_path'])
LAUNCHER_SHORTCUT = os.path.normpath(settings['paths']['launcher_shortcut_path'])
# Convert colors from settings.toml to colorama.Fore attributes
DEFAULT_TEXT_COLOR = settings['color_map']['default_text_color']

DEFAULT_MAP_COLOR = settings['color_map']['default_map_color']
ADDED_MAP_COLOR = settings['color_map']['added_map_color']
ZIP_NAME_COLOR = settings['color_map']['zip_name_color']
NUMBER_COLOR = settings['color_map']['number_color']
CONFIG_NAME_COLOR = settings['color_map']['config_name_color']
CONFIG_VALUE_COLOR = settings['color_map']['config_value_color']

SUCCESS_COLOR = settings['color_map']['success_color']
ERROR_COLOR = settings['color_map']['error_color']
ERR_SUCC_COLOR = settings['color_map']['error_or_success_text_color']
# Define the color map for map listings
color_map = {
    "default_map_color": DEFAULT_MAP_COLOR,
    "added_map_color": ADDED_MAP_COLOR,
    "zip_name_color": ZIP_NAME_COLOR  
}