# Commands for command line input
__author__ = "Matteo Golin"

# Imports
import argparse
import commands.validators as v

# Constants
DESCRIPTION = ""

# Parsers
parser = argparse.ArgumentParser(description=DESCRIPTION)
subparsers = parser.add_subparsers(dest="subcommand")

# Main commands

# Sub commands

# Console interface commands
console_options = subparsers.add_parser("console")

# Initial sort
initial_sort = subparsers.add_parser("initial-sort")

# Create config commands
set_config = subparsers.add_parser("config")

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
modify_config = subparsers.add_parser("mod-config")

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
add_directory = subparsers.add_parser("add-directory")

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
