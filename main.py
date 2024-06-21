from functions import *


class CustomArgumentParser(argparse.ArgumentParser):
    def print_help(self):
        help_text = super().format_help()
        usage_examples = (
            f"\n[bold {DEFAULT_MAP_COLOR}]Usage Examples:[/bold {DEFAULT_MAP_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  List maps:[/{DEFAULT_TEXT_COLOR}]      BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]list[/bold {CONFIG_VALUE_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  Sync maps:[/{DEFAULT_TEXT_COLOR}]      BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]sync[/bold {CONFIG_VALUE_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  Pick map:[/{DEFAULT_TEXT_COLOR}]       BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]pick[/bold {CONFIG_VALUE_COLOR}] [{ZIP_NAME_COLOR}]<map_name_or_id>[/{ZIP_NAME_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  Open Paths:[/{DEFAULT_TEXT_COLOR}]     BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]open[/bold {CONFIG_VALUE_COLOR}] [{ZIP_NAME_COLOR}]<option>[/{ZIP_NAME_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  Run exe/lnk:[/{DEFAULT_TEXT_COLOR}]    BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]run[/bold {CONFIG_VALUE_COLOR}] [{ZIP_NAME_COLOR}]<option>[/{ZIP_NAME_COLOR}]\n"
            f"[{DEFAULT_TEXT_COLOR}]  Update Program:[/{DEFAULT_TEXT_COLOR}] BMPMapSwitcher [bold {CONFIG_VALUE_COLOR}]update[/bold {CONFIG_VALUE_COLOR}]\n"
        
        )
        #console.print(Text.from_markup(help_text))
        console.print(Text.from_markup(usage_examples))

    def error(self, message):
        self.print_help()
        console.print(f"[bold red]{message}[/bold red]")
        os.sys.exit(2)
 
def main():
    parser = CustomArgumentParser(description=f"Map Management Script")
    parser.add_argument('command', choices=['list', 'pick', 'sync', 'open', 'run', 'update'], help=f"Command to execute")
    parser.add_argument('map_identifier', nargs='?', default=None)
    
    # If no arguments are provided, show a custom message instead of the default help message
    if len(os.sys.argv) == 1:
        console.print(f"[{DEFAULT_TEXT_COLOR}]No command provided. Use one of the following commands:[/{DEFAULT_TEXT_COLOR}]")
        parser.print_help()
        os.sys.exit(1) 
    
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
