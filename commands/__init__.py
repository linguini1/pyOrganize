# Command line argument parsing
__author__ = "Matteo Golin"

# Imports
import argparse

# Constants
SUBCOMMMAND = "subcommand"  # Subcommand tag
DESCRIPTION = "Configure the sorter's settings."

parser = argparse.ArgumentParser(description=DESCRIPTION)
subparser = parser.add_subparsers(dest=SUBCOMMMAND)

# Sort as soon as the program is run
parser.add_argument(
    "--sort",
    help="Sorts the watched directory on program run.",
    action="store_true"
)

# Clear all configurations
parser.add_argument(
    "--wipe",
    help="Clears all previous configurations.",
    action="store_true"
)

# Set the home directory
parser.add_argument(
    "-home",
    help="Sets the home directory where files will be sent to be sorted. This directory should nest all sorted "
         "subdirectories.",
    type=str,
    metavar="path"
)

# Set the watched directory
parser.add_argument(
    "-watch",
    help="Sets the directory that will be watched for files to be sorted.",
    metavar="path",
    type=str,
)

# Set the ignore symbol
parser.add_argument(
    "-i",
    help="Sets the symbol that denotes a file which shouldn't be moved from the watched directory.",
    type=str,
    metavar="symbol"
)

# Add a directory to the directory list
dir_adder = subparser.add_parser(
    "add",
    description="Adds a directory and its tags to the list of directories in use. If the directory is already in use, "
                "it will add the passed tags to the proper directory.",
)

dir_adder.add_argument(
    "directory",
    help="Specifies the directory to be added.",
    type=str,
    metavar="directory"
)

dir_adder.add_argument(
    "tags",
    help="Specifies a list of tags to be associated with the directory.",
    type=str,
    nargs="+",
    metavar="tag"
)

# Remove a directory from the directory list
dir_remover = subparser.add_parser("remove-dir")

dir_remover.add_argument(
    "directories",
    help="Takes the name of one or more directories to be removed from the list of directories in use.",
    nargs="+",
    metavar="directory"
)

# Remove a tag from the tag list or from a specific directory
tag_remover = subparser.add_parser(
    "remove-tag",
    description="Removes a tag for all directories or specified directories."
)

tag_remover.add_argument(
    "tag",
    help="The tag that will be removed.",
    type=str,
    nargs=1,
    metavar="tag",
)

tag_remover.add_argument(
    "-d",
    help="Specifies directories from which the tag is to be removed.",
    nargs="+",  # Multiple directories can be specified
    metavar="directory",
    type=str
)

# Show config settings
display = subparser.add_parser("display")

display.add_argument(
    "selection",
    help="Selects which information from the config file should be displayed.",
    type=str,
    choices=["tags", "used-dirs", "available-dirs"],
)
