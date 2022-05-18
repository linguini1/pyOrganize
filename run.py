# Main file to run the program
__author__ = "Matteo Golin"

# Imports
from classes.application import Application
from classes.config import Config
from classes.console import Console
from classes.directory import Directory
from classes.handler import WatchDir
from commands import parser

# Get arguments
arguments = parser.parse_args()
arguments = vars(arguments)  # Convert to dictionary
subcommand = arguments.get("subcommand")

print(arguments)

if subcommand == "config":
    config = Config(
        watch_dir=arguments.get("watch-dir"),
        ignore_char=arguments.get("ignore-char"),
        ignored_names=arguments.get("ignored-names")
    )
    config.save({})
    print("Config file successfully created.")
    quit()

app = Application()

if subcommand == "add-directory":
    Directory(
        path=arguments.get("path"),
        tags=arguments.get("tags"),
        recursive=arguments.get("-recursive-tags"),
        parent_tags=arguments.get("-parent-tags")
    )
    app.clean_up()
    quit()

if subcommand == "mod-config":
    app.update_config(arguments)

if subcommand == "console":
    console = Console(app)
    console.start()

# File save event logic
if __name__ == "__main__":
    watcher = WatchDir(app)
    watcher.run(initial_sort=(subcommand == "initial-sort"))
