# Class for interaction via the console
__author__ = "Matteo Golin"

# Imports
import os
from .directory import Directory
from .application import Application

# Constants
YES = ["y", "yes", "yeah", "yep"]
QUIT = ["quit", "q", "exit"]


# Class
class Console:

    """Holds all the functions required to operate the application via the console."""

    def __init__(self, app: Application):
        self.app = app

    def __get_specific_directory(self) -> Directory | None:

        """Returns the directory specified by the user."""

        cont = "y"

        while cont.lower() in YES:

            path = input("Enter a directory: ")

            if os.path.isdir(path):

                db_result = self.app.get_dir(path)

                # Return existing database directory
                if db_result is not None:
                    return db_result

                # If database has no existing directory, then create a new one
                else:
                    print(f"{path} does not exist in the database. Creating new directory object...")
                    return Directory(path=path, tags=[])

            else:
                print("Directory does not exist. Do you want to enter a new directory? (y/n): ")

        return None

    def __search_for_directory(self) -> Directory | None:

        """Allows the user to search the directory database with directory name, and select a result."""

        while True:
            name = input("Enter a directory name: ")  # Get search name
            results = self.app.search_dirs(name)  # Perform search

            # Reprompt for keyword
            if len(results) == 0:
                cont = input("There are no matching directories. Continue? (y/n): ")

                # No continue, return immediately
                if cont.lower() not in YES:
                    return None

            # Return only option
            elif len(results) == 1:
                print(f"The only match is {results[0].path}. Selecting this option...")
                return results[0]

            # Move on to selection
            else:
                break

        # List directory results
        for index, directory in enumerate(results):  # List results
            print(f"{index + 1} - {directory.path}")

        while True:
            selection = input("Select directory using number (q to quit): ")  # Get choice

            # If the user selects to quit, quit immediately
            if selection.lower() in QUIT:
                return None

            try:
                selection = int(selection)  # Convert to usable integer

                if (selection - 1) in range(len(results)):  # Check if selection exceeds option range
                    return results[selection - 1]  # Return the chosen directory

                else:
                    print("Invalid selection.")

            except ValueError:
                print("That is not a number.")

    @staticmethod
    def __get_tags() -> list[str]:

        """Gets tags from user input."""

        tags = input("Enter comma separated tags (<tag>, <tag>...): ")
        return tags.split(",")

    def get_directory(self) -> Directory | None:

        """Allows the user to get a directory by path or by searching its name in the database."""

        search_method = "Search directories by name or path (name/path): "

        while True:
            if search_method.lower() == "path":
                return self.__get_specific_directory()
            elif search_method.lower() == "name":
                return self.__search_for_directory()
            else:
                print("Invalid search method.")

    def add_tags_to_directory(self):

        """Allows the user to select a directory and add tags to it."""

        # Get directory
        chosen_directory = self.get_directory()

        if chosen_directory is not None:  # User did not quit selection

            tags = self.__get_tags()
            chosen_directory.add_tags(tags)
            print(f"{tags} successfully added to {chosen_directory.path}.")

    def add_directory(self):

        """Creates a new directory object."""

        while True:
            path = input("Enter directory path: ")

            if not os.path.isdir(path):
                print("Invalid directory.")
            else:
                break

        tags = self.__get_tags()

        return Directory(path=path, tags=tags)

    def start(self):

        """Starts the console interface."""

        print("Not implemented.")  # TODO

