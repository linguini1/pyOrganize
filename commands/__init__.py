# Commands for command line input
__author__ = "Matteo Golin"

# Imports
import argparse
import commands.validators as v

# Constants
HELP_STATEMENTS = {
    "parser": None,
    "subcommands": None,
    "add-directory": "Adds a directory or multiple directories to the configurations file. If directory already exists"
                     "in config file, the tags are updated accordingly.",
    "initial-sort": "Runs an initial sort in the watched directory.",
    "console": "Starts the console interface at runtime.",
    "config": "Creates a new configurations file. This overwrites any existing configurations.",
    "mod-config": "Allows modification of the configurations file.",
}

# Parsers
parser = argparse.ArgumentParser(description=HELP_STATEMENTS["parser"])
subparsers = parser.add_subparsers(dest="subcommand", help=HELP_STATEMENTS["subcommands"])

# Main commands

# Sub commands

# Console interface commands
console_options = subparsers.add_parser("console", help=HELP_STATEMENTS["console"])

# Initial sort
initial_sort = subparsers.add_parser("initial-sort", help=HELP_STATEMENTS["initial-sort"])

# Create config commands
set_config = subparsers.add_parser("config", help=HELP_STATEMENTS["config"])

set_config.add_argument(
    "watch-dir",
    help="Sets the directory that should be watched by the sorter.",
    type=v.Directory,
)

set_config.add_argument(
    "ignore-char",
    default="!",
    help="Sets the character to be included in filenames that should be ignored by the sorter.",
    type=v.Char,
)

set_config.add_argument(
    "ignored-names",
    nargs="*",
    help="Sets a list of directory names that should be ignored by the sorter when indexing.",
)

# Modify config commands
modify_config = subparsers.add_parser("mod-config", help=HELP_STATEMENTS["mod-config"])

modify_config.add_argument(
    "-watch-dir", "-w",
    help="Resets the directory that should be watched by the sorter.",
    type=v.Directory,
)

modify_config.add_argument(
    "-ignore-char", "-i",
    help="Resets the character to be included in filenames that should be ignored by the sorter.",
)

modify_config.add_argument(
    "-ignored-names", "-in",
    help="Appends a list of directory names that should be ignored by the sorter when indexing to the config file.",
    nargs="*",
)

# Add directory
add_directory = subparsers.add_parser("add-directory", help=HELP_STATEMENTS["add-directory"])

add_directory.add_argument(
    "path",
    help="Path of directory to be added.",
    type=v.Directory,
)

add_directory.add_argument(
    "tags",
    default=list(),
    help="List of tags associated with the directory.",
    nargs="*",
)

add_directory.add_argument(
    "-recursive-tags", "-rt",
    default=False,
    help="Adds tags recursively to all subdirectories of the added directory.",
    action="store_true",
)

add_directory.add_argument(
    "-parent-tags", "-pt",
    default=False,
    help="Adds tags from the parent directory to the directory.",
    action="store_true",
)
