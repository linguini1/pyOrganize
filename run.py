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

print(f"DEBUG: {arguments}")

if subcommand == "config":
    config = Config(
        watch_dir=arguments.get("watch-dir"),
        ignore_char=arguments.get("ignore-char"),
        ignored_names=arguments.get("ignored-names")
    )
    config.save({})
    print("Config file successfully created.\n")
    print(config)
    quit()

app = Application()

if subcommand == "add-directory":

    # Unpack args
    path = arguments.get("path")
    tags = arguments.get("tags")
    recursive = arguments.get("recursive_tags")
    parent_tags = arguments.get("parent_tags")

    # Check if directory exists before creating a new one
    directory = Directory.directories.get(path)

    if directory:
        directory.add_tags(tags, recursive)
        if parent_tags:
            directory.add_parent_tags(recursive)
    else:
        directory = Directory(
            path=path,
            tags=tags,
            recursive=recursive,
            parent_tags=parent_tags
        )

    print(f"Director{'ies' if recursive else 'y'} successfully added.\n")
    print(directory)
    app.clean_up()
    quit()

if subcommand == "mod-config":
    app.update_config(arguments)
    print("Config successfully modified.\n")
    print(app.config)

if subcommand == "console":
    console = Console(app)
    console.start()

# File save event logic
if __name__ == "__main__":
    watcher = WatchDir(app)
    watcher.run(initial_sort=(subcommand == "initial-sort"))
