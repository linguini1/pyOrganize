# Config class
__author__ = "Matteo Golin"

# Imports
import json
import os

# Constants
CONFIG_FILENAME = "config.json"


# Class
class Config:

    filename = CONFIG_FILENAME

    def __init__(self, watch_dir: str, ignored_names: list[str], ignore_char: str):
        self.watch_dir = watch_dir
        self.ignored_names = ignored_names
        self.ignore_char = ignore_char

    def save(self, directories: dict):

        """Save all directories to the config file."""

        with open(self.filename, "w") as config:

            data = {
                "watch_dir": self.watch_dir,
                "ignored_names": self.ignored_names,
                "ignore_char": self.ignore_char,
                "directories": directories,
            }

            json.dump(data, config, default=lambda o: o.to_JSON())  # Lambda allows classes to be serialized

    def delete(self):

        """Deletes the config file."""

        current_directory = os.getcwd()
        os.remove(f"{current_directory}\\{self.filename}")

    def __repr__(self):
        representation = f"Watch: {self.watch_dir} Ignore Character: {self.ignore_char}\nIgnored Names:\n"
        for name in self.ignored_names:
            representation += f"{name}\n"
        return f"Config(\n{representation})"
