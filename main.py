from functions import *

def main():
    class CustomArgumentParser(argparse.ArgumentParser):
        def format_help(self):
            help_text = super().format_help()
            usage_examples = (
                f"\n[{SUCCESS_COLOR}]Usage Examples:[/{SUCCESS_COLOR}]\n"
                f"[{DEFAULT_TEXT_COLOR}]  List maps:[/{DEFAULT_TEXT_COLOR}] [{CONFIG_VALUE_COLOR}]python script.py list[/{CONFIG_VALUE_COLOR}]\n"
                f"[{DEFAULT_TEXT_COLOR}]  Sync maps:[/{DEFAULT_TEXT_COLOR}] [{CONFIG_VALUE_COLOR}]python script.py sync[/{CONFIG_VALUE_COLOR}]\n"
                f"[{DEFAULT_TEXT_COLOR}]  Pick a map by name or ID:[/{DEFAULT_TEXT_COLOR}] [{CONFIG_VALUE_COLOR}]python script.py pick <map_name_or_id>[/{CONFIG_VALUE_COLOR}]\n"
                f"[{DEFAULT_TEXT_COLOR}]  Open settings:[/{DEFAULT_TEXT_COLOR}] [{CONFIG_VALUE_COLOR}]python script.py open settings[/{CONFIG_VALUE_COLOR}]\n"
                f"[{DEFAULT_TEXT_COLOR}]  Run the server:[/{DEFAULT_TEXT_COLOR}] [{CONFIG_VALUE_COLOR}]python script.py run server[/{CONFIG_VALUE_COLOR}]\n"
            )
            return help_text + usage_examples

    parser = CustomArgumentParser(description=f"{DEFAULT_TEXT_COLOR}Map Management Script[/{DEFAULT_TEXT_COLOR}]")
    parser.add_argument('command', choices=['list', 'pick', 'sync', 'open', 'run', 'update'], help=f"[{DEFAULT_TEXT_COLOR}]Command to execute[/{DEFAULT_TEXT_COLOR}]")
    parser.add_argument('map_identifier', nargs='?', default=None)
    args = parser.parse_args()

    if args.command == 'sync':
        sync_maps()
    elif args.command == 'list':
        list_maps()
    elif args.command == 'pick':
        if args.map_identifier:
            pick_map(args.map_identifier)
        else:
            exc_handler("error", f"Please provide the map name or ID to pick.")
    elif args.command == 'open':
        if args.map_identifier:
            open_paths(args.map_identifier)
        else:
            exc_handler("error", f"Invalid Option (choose from: 'settings', 'script', 'maps' or 'config' )")
    elif args.command == 'run':
        if args.map_identifier:
            run_execs(args.map_identifier)
        else:
            exc_handler("error", f"Please provide the option to run (choose from: 'launcher', 'tunnel' or 'server')")    
    elif args.command == 'update':
        update_script()
    else:
        exc_handler("error", f"Unknown command")

if __name__ == "__main__":
    main()
