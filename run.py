# Main file to run the program
__author__ = "Matteo Golin"

# Imports
from pprint import pprint  # Convenient for debugging JSOn
from commands import parser, SUBCOMMMAND
from functions.configure import start_config, wipe_config, add_dir, remove_dir, remove_tag, LABELS, DISPLAY
from functions.watch import WatchDir

# Parse arguments
args = parser.parse_args()
passed_args = vars(args)  # Dictionary version to prevent lookup error

if args.wipe:
    wipe_config()

# Variables to be set by the user (manually set for testing)
# args.home = "C:/Users/golin/Downloads/testSorted"
# args.watch = "C:/Users/golin/Downloads/testDir"
# args.i = "!"

# Start up config
conf = start_config(args.home, args.watch, args.i)
print("Config file loaded!")

# Add and remove required directories
if passed_args.get(SUBCOMMMAND) == "add":
    add_dir(args.directory[0], args.tags, conf)

if passed_args.get(SUBCOMMMAND) == "remove-dir":
    for dir_name in args.directories:
        remove_dir(dir_name, conf)

# Remove tags
if passed_args.get(SUBCOMMMAND) == "remove-tag":
    remove_tag(args.tag[0], passed_args.get("d"), conf)


# Displaying information
if passed_args.get(SUBCOMMMAND) == "display":
    DISPLAY[passed_args.get("selection")](conf)  # Calls corresponding display function

# pprint(conf)

# File save event logic
if __name__ == "__main__" and not passed_args.get("subcommand"):  # Doesn't run when configurations are being done
    watcher = WatchDir(conf)
    watcher.run(initial_sort=args.sort)
