# Contains functions to change program config
__author__ = "Matteo Golin"

# Imports
import json
import os
from typing import Iterator

# Constants
CONFIG_FILE = "./config/config.json"
CONFIG_FILENAME = "config.json"

# Label names
LABELS = {
    "homeDir": "home",
    "watchedDir": "watch",
    "ignoreSymbol": "ignore",
    "dirPaths": "directory paths",
    "tags": "tags"
}

# User input
POSITIVE_RESPONSES = ["y", "yes", "sure", "yeah"]
NEGATIVE_RESPONSES = ["n", "no", "nope"]


# Check for config file
def config_exists() -> bool:

    """Returns True if a config file exists, returns False if not."""

    return os.path.isfile(CONFIG_FILE)


# Write config file
def create_config(home: str, watch: str, ignore_symbol: str):

    """
    Creates a config.json file within the config directory that contains static values.
    """

    # Error catching
    if not home:
        raise ValueError("Please specify a home directory.")
    elif not watch:
        raise ValueError("Please specify a directory to watch.")
    elif not ignore_symbol:
        raise ValueError("Please specify a symbol to denote ignored files.")

    # Set static values in config
    conf = {
        LABELS["homeDir"]: home,
        LABELS["watchedDir"]: watch,
        LABELS["ignoreSymbol"]: ignore_symbol,
        LABELS["tags"]: {},
        LABELS["dirPaths"]: {},
    }

    # Write config to file
    with open(CONFIG_FILE, 'w') as file:
        json.dump(conf, file)


# Read config file
def load_config() -> dict:

    """Returns the config value as a dictionary object."""

    with open(CONFIG_FILE, 'r') as file:
        conf = json.load(file)

    return conf


def start_config(home: str, watch: str, ignore_symbol: str) -> dict:

    """Creates config if there is none, and returns the loaded config as a dictionary."""

    if not config_exists():
        create_config(home, watch, ignore_symbol)

    # Load config
    config = load_config()

    # Track if changes were made
    changes_made = False
    home_changed = False

    # If watch directory was changed, update it
    if watch != config[LABELS["watchedDir"]] and watch:
        config[LABELS["watchedDir"]] = watch
        changes_made = True

    # If ignore symbol was changed, update it
    if ignore_symbol != config[LABELS["ignoreSymbol"]] and ignore_symbol:
        config[LABELS["ignoreSymbol"]] = ignore_symbol
        changes_made = True

    # If the home directory was changed, start a fresh config using the new home dir
    if home != config[LABELS["homeDir"]] and home:
        new_ignore = config[LABELS["ignoreSymbol"]]
        new_watch = config[LABELS["watchedDir"]]
        create_config(home, new_watch, new_ignore)
        home_changed = True

    if changes_made and not home_changed:  # Just update config and reload isn't necessary
        update_config(config)
    elif home_changed:  # Home directory change requires reload
        config = load_config()

    update_paths(config)  # Update all directories

    return config


# Wipe config file
def wipe_config():

    """Deletes the config file after getting user confirmation."""

    if not config_exists():  # File can't be deleted if it doesn't exist
        raise FileNotFoundError("Config file does not exist.")

    while True:
        response = input("Are you sure you want to wipe all configurations? (y/n): ")

        if response.lower() in POSITIVE_RESPONSES:  # Yes
            print("Wiping...")
            os.remove(CONFIG_FILE)
            print("Wiped successfully.")
            quit()  # The program can't continue without a config file

        elif response.lower() in NEGATIVE_RESPONSES:  # No
            print("Wipe aborted.")
            break


# Update config file
def update_config(config_object: dict):

    """Updates the disk copy of the config file with changes to the config object."""

    with open(CONFIG_FILE, 'w') as file:
        json.dump(config_object, file)


# Update paths
def get_dir_tree(directory: str) -> Iterator:

    """Gets all the subdirectories of a given directory."""

    return os.walk(directory)


def update_paths(config_object: dict):

    """Update stored paths within the config file."""

    home_dir = config_object[LABELS["homeDir"]]

    dir_paths = {}  # Dictionary to record directory paths
    directory_tree = get_dir_tree(home_dir)

    # Store directory paths
    for path, _, _ in directory_tree:

        dir_name = path.split("\\")[-1]  # Get directory name
        path = path.split(home_dir)[1].replace("\\", "/")  # Replace the double backslash and start path from home dir

        # If there is more than one directory in the tree with that name, store path to an array
        if not dir_paths.get(dir_name):  # Doesn't exist yet
            dir_paths[dir_name] = [path]
        else:  # Duplicate name
            dir_paths[dir_name].append(path)

    # Write paths to config file
    config_object[LABELS["dirPaths"]] = dir_paths
    update_config(config_object)


def get_matching_dirs(dir_name: str, config_object: dict) -> list[str] | None:

    """Returns a list of all directory paths where the terminating directory matches the passed directory name."""

    return config_object[LABELS["dirPaths"]].get(dir_name)


def user_select_dir(dir_list: list[str]) -> list:

    """Returns the path of the directory the user selects."""

    dir_name = dir_list[0].split("/")[-1]

    # Info message
    print(f"The directory {dir_name} has multiple matching paths.")

    # Print directory options
    for _ in range(len(dir_list)):
        print(f"{_ + 1} - {dir_list[_]}")
    print(f"{len(dir_list) + 1} - All of the above.")

    # Get choice
    while True:
        choice = input("Which one did you mean specifically? Type the associated number: ")

        try:
            choice = int(choice)

            # Within range of list
            if 1 <= choice <= len(dir_list):
                return [dir_list[choice - 1]]
            elif choice == len(dir_list) + 1:  # All of the above
                return dir_list

        except ValueError:  # Not integer
            pass


def search_dirs(dir_name: str, config_object: dict) -> list | None:

    """Searches for directories matching the dir name and narrows down to one result."""

    matching_dirs = get_matching_dirs(dir_name, config_object)

    # No matching directories
    if not matching_dirs:
        return None

    # More than one directory with that name
    elif len(matching_dirs) > 1:
        return user_select_dir(matching_dirs)

    # One directory
    else:
        return matching_dirs


# Add dir
def user_select_nested(selected_dirs: list, config_object: dict) -> list:

    """
    Allows the user to select whether or not tags should be applied to all subdirectories of the directories they
    selected.

    Returns a modified selected_dirs list that contains all chosen subdirectories.
    """

    while True:
        choice = input("Do you want to apply these tags to all subdirectories of your selected directories? (y/n): ")

        if choice.lower() in POSITIVE_RESPONSES:

            home_dir = config_object[LABELS["homeDir"]]
            subdirectories = []

            for selected_dir in selected_dirs:  # Add all subdirectories
                subdirectory_tree = get_dir_tree(home_dir + selected_dir)
                for path, _, _ in subdirectory_tree:
                    subdirectory = path.split(home_dir)[1].replace("\\", "/")
                    subdirectories.append(subdirectory)

            selected_dirs.extend(subdirectories)

            return selected_dirs

        elif choice.lower() in NEGATIVE_RESPONSES:
            return selected_dirs  # Return original

        print("Invalid answer.")  # Neither yes nor no was entered


def add_dir(dir_name: str, tags: list, config_object: dict):

    """Takes a directory name and its tags and adds it as an available directory to the config."""

    selected_dirs = search_dirs(dir_name, config_object)

    if not selected_dirs:  # No directory found with matching name
        print(f"No such directory as {dir_name}.")
        return None

    tags_dict = config_object[LABELS["tags"]]

    # Query user if tags should be added to all subdirectories of the given directory
    selected_dirs = user_select_nested(selected_dirs, config_object)

    # Actual adding
    for selected_dir in selected_dirs:

        # List directory under its tags
        for tag in tags:

            tag_exists = tags_dict.get(tag)

            # If the tag exists, add directory to directories with that tag
            if tag_exists:
                directories = set(tags_dict[tag])  # Convert to set
                directories.add(selected_dir)  # Add directory to set to ensure no duplication
                tags_dict[tag] = list(directories)  # Convert set to list and replace under tag

            # If tag doesn't exist, initialize array
            else:
                tags_dict[tag] = [selected_dir]

    # Update hard copy config
    update_config(config_object)

    print("Successfully added the following tags:")
    for tag in tags:
        print(f"- {tag}")
    print("to the following directories:")
    for directory in selected_dirs:
        print(f"- {directory}")


# Remove dir
def remove_dir(dir_name: str, config_object: dict):

    """Makes a directory unavailable to the config (strips it of its tags)."""

    selected_dirs = search_dirs(dir_name, config_object)

    if not selected_dirs:  # No directory with matching name
        print(f"No such directory as {dir_name}.")
        return None

    # Remove all instances of that directory
    for selected_dir in selected_dirs:  # All selected dirs

        tags = list(config_object[LABELS["tags"]].keys())  # List of all tags

        for tag in tags:  # Remove from each tag
            for directories in config_object[LABELS["tags"]][tag]:
                if selected_dir in directories:
                    config_object[LABELS["tags"]][tag].remove(selected_dir)

                    # If a tag is empty, delete it completely
                    if not config_object[LABELS["tags"]][tag]:
                        config_object[LABELS["tags"]].pop(tag)

        print(f"Removed {selected_dir}.")

    # Update hard copy config
    update_config(config_object)


# Remove tags
def remove_tag(tag: str, directories: list, config_object: dict):

    """Removes a tag from the config file. Can be removed for all dirs or for specific dirs."""

    # Remove all instances of tag
    if not directories:
        config_object[LABELS["tags"]].pop(tag)
        update_config(config_object)
        return None

    for directory in directories:

        # Remove from a specific directory
        selected_dirs = search_dirs(directory, config_object)  # Matching directories

        for selected_dir in selected_dirs:
            config_object[LABELS["tags"]][tag].remove(selected_dir)

    update_config(config_object)


# Display tags
def display_tags(config_object: dict):

    """Prints all tags from the config file to the console."""

    deco = "-" * 30
    print(f"{deco}TAGS{deco}")

    for tag, directories in config_object[LABELS["tags"]].items():
        print(f"{tag}")
        for directory in directories:
            print(f"  - {directory}")


def display_dirs_in_use(config_object: dict):

    """Displays the list of available directories in the config file to the console."""

    directories = set()

    for dirs in config_object[LABELS["tags"]].values():
        directories.update(set(dirs))

    deco = "-" * 30
    print(f"{deco}DIRECTORIES IN USE{deco}")

    for directory in directories:
        print(f"- {directory}")


def display_all_dirs(config_object: dict):

    """Prints all directories listed under the home directory to the console."""

    deco = "-" * 30
    print(f"{deco}AVAILABLE DIRECTORIES{deco}")

    for directories in config_object[LABELS["dirPaths"]].values():
        for directory in directories:

            # Home directory is stored as empty string but that's not intuitive for display
            if directory == "":
                directory = "/"

            print(f"- {directory}")


# Function bundles
DISPLAY = {
    "tags": display_tags,
    "available-dirs": display_all_dirs,
    "used-dirs": display_dirs_in_use,
}
