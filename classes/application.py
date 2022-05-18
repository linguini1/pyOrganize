# Main application class
__author__ = "Matteo Golin"

# Imports
from .config import Config
from .directory import Directory
import utils as u
import json
import os


# Class
class Application:

    def __init__(self, config: Config = None):

        # Load config or use passed parameters
        if config is None:
            self.config = self.load_config()
        else:
            self.config = config

    # Methods
    def create_sub_dirs(self, root: str):

        """
        Creates directory objects for all the subdirectories (and their subdirectories, etc.) of the passed
        directory.
        """

        subdir_list = os.walk(root)

        for path, dirs, files in subdir_list:
            if os.path.isdir(path) and any(name in path for name in self.config.ignored_names):
                Directory(
                    path=path,
                    tags=[],
                )

    def clean_up(self):

        """Shuts down the application, saving the configurations."""

        self.config.save(Directory.directories)

    def sort_file(self, file_path: str):

        """Sorts the passed file into its proper place, ignoring files that contain ignored characters."""

        if self.config.ignore_char not in file_path:
            chosen_directory = self.get_best_dir(file_path)

            # If there are 0 matching tags, do not move the file
            if not chosen_directory.matching_tags(file_path) == 0:
                chosen_directory.nest_file(file_path)

    def update_config(self, commandline_args: dict):

        """Updates the config information with the commandline argument values."""

        watch_dir = commandline_args.get("-watch-dir")
        ignore_char = commandline_args.get("-ignore-char")
        ignored_names = commandline_args.get("-ignored-names")

        if watch_dir:
            self.config.watch_dir = watch_dir

        if ignore_char:
            self.config.ignore_char = ignore_char

        if ignored_names:
            self.config.ignored_names.extend(ignored_names)

    # Static methods
    @staticmethod
    def get_best_dir(file_path: str) -> Directory:

        """Returns the Directory object that has the most matching tags/is the best fit."""

        filename = u.filename(file_path)
        all_matches = []

        for directory in Directory.directories.values():
            matching_tags = directory.matching_tags(filename)  # Get num of matching tags
            all_matches.append((matching_tags, directory))  # Add tuple to list

        return max(all_matches, key=lambda x: x[0])[1]

    @staticmethod
    def search_dirs(dir_name: str) -> list[Directory]:

        """Returns a list of directories whose paths contain the keyword/name passed."""

        matches = []  # Store all matches

        for directory in Directory.directories:
            if dir_name in directory.path.split("\\")[-1]:  # Check the last part of the path to avoid duplicates
                matches.append(directory)

        if len(matches) == 0:
            raise NotADirectoryError(f"No directories matching name {dir_name} can be found.")
        else:
            return matches

    @staticmethod
    def get_dir(dir_path: str) -> Directory:

        """Returns the directory object with the matching path."""

        directory = Directory.directories.get(dir_path)

        if directory:  # If found
            return directory

        raise NotADirectoryError(f"The directory {dir_path} cannot be found.")

    @staticmethod
    def load_config() -> Config:

        """Loads the config from a previously saved config file."""

        # Check if file exists or raise error
        if not os.path.exists(Config.filename):
            raise FileNotFoundError("No config file exists. Please create a config file.")

        with open(Config.filename, "r") as config:
            data = json.load(config)

        for directory_path in data["directories"]:

            # Create a directory object for each directory
            Directory(
                path=directory_path,
                tags=data["directories"][directory_path]["tags"]
            )

        # Return a configurations object
        return Config(
            watch_dir=data["watch_dir"],
            ignored_names=data["ignored_names"],
            ignore_char=data["ignore_char"],
        )
