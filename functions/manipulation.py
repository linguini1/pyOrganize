# Contains functions for file manipulation
__author__ = "Matteo Golin"

# Imports
import os
from .configure import LABELS
from collections import Counter


def get_matching_tags(filename: str, config_object: dict) -> list:

    """Returns all tags that the filename matches as a list."""

    matching_tags = []

    for tag in config_object[LABELS["tags"]].keys():

        if tag in filename.lower():
            matching_tags.append(tag)

    return matching_tags


def which_dir(matching_tags: list, config_object: dict) -> list | None:

    """Based on matching tags, returns the directory with the most matching tags."""

    flattened_matches = []  # Stores the list of directories under each matching tag

    # Appends list of directories under tag
    for tag in matching_tags:
        flattened_matches.extend(config_object[LABELS["tags"]][tag])

    counter = Counter(flattened_matches)
    top_matches = counter.most_common()

    if not top_matches:  # No matching directories
        return None
    else:
        highest_count = top_matches[0][1]  # Get the count required to be a best match

        # Return all directories that have a count matching the highest count
        highest = filter(lambda directory: directory[1] == highest_count, top_matches)
        return [directory[0] for directory in list(highest)]


def move_file(filepath: str, config_object: dict):

    """Moves the file to its best match directory."""

    filename = filepath.split("/")[-1]  # Get filename

    matching_tags = get_matching_tags(filename, config_object)
    best_dirs = which_dir(matching_tags, config_object)

    # No match
    if not best_dirs:
        return None  # Don't move file

    # One match
    elif len(best_dirs) == 1:
        best_dir = best_dirs[0]

    # Multiple matches
    else:

        # Pick the match that is highest up the directory tree
        lowest_count = best_dirs[0].count("/")  # Initialize lowest count using first option
        highest_dir = best_dirs[0]

        for directory in best_dirs[1:]:

            # If / is lower, it's higher up the tree
            if directory.count("/") < lowest_count:
                highest_dir = directory

        best_dir = highest_dir

    # Move file
    home_dir = config_object[LABELS["homeDir"]]
    os.rename(filepath, f"{home_dir}{best_dir}/{filename}")  # Change old path to path to best dir

    # Log file movement to console
    print(f"Moved {filename} to {home_dir}{best_dir}.")
