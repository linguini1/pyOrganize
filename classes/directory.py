from __future__ import annotations

# Directory class for representing directories
__author__ = "Matteo Golin"

# Imports
import os
from utils.logging import log_file_movement

# Types
TagList = list[str]


# Class
class Directory:

    directories = {}

    def __init__(self, path: str, tags: TagList, recursive: bool = False, parent_tags: bool = False):
        self.path = path
        self.tags = set(tags)

        # Recursive tags
        if recursive:
            self.__add_tags_children(list(self.tags))

        # Add parent tags
        if parent_tags:
            self.add_parent_tags(recursive=recursive)

        # Save directory to master dict of directories
        self.directories[self.path] = self

    # Methods
    def __add_tags_children(self, tags: str | TagList):

        """Adds tags to child directories."""

        subdirectories = os.walk(self.path)

        for dir_path, _, _ in subdirectories:
            directory = self.directories.get(dir_path)

            if directory:  # Already exists as object
                directory.add_tags(tags)
            else:  # Must be created
                Directory(
                    path=dir_path,
                    tags=tags
                )

    def add_tags(self, tags: str | TagList, recursive: bool = False):

        """Adds a tag or multiple tags to the tag list."""

        # Convert to list if single tag is passed as string
        if type(tags) is str:
            tags = [tags]

        if recursive:
            self.__add_tags_children(tags)

        else:
            self.tags.update(tags)

    def add_parent_tags(self, recursive: bool = False):

        """Adds tags of the parent directory to itself, and its children if recursive mode is selected."""

        parent_path = self.path.split("\\")[:-1]
        parent = self.directories.get(parent_path)

        if parent:
            self.add_tags(parent.tags, recursive=recursive)
        else:
            raise NotADirectoryError(
                "Parent directory is not specified in the configurations file. Please add the parent directory "
                "separately and try again."
            )

    def remove_tag(self, tag_name: str):

        """Removes tag from tags list."""

        self.tags.remove(tag_name)

    def nest_file(self, file_path: str):

        """Nests the passed file within itself."""

        file = file_path.split("\\")[-1]
        file_name, file_ext = file.split(".")

        # Increase counter on filename if file already exists in directory
        counter = 1
        counted_file_name = file_name
        while os.path.exists(f"{self.path}\\{counted_file_name}.{file_ext}"):
            counted_file_name = f"{file_name} ({counter})"
            counter += 1

        new_path = f"{self.path}\\{counted_file_name}.{file_ext}"
        os.rename(file_path, new_path)

        # Logging
        log_file_movement(file_path, new_path)

    def matching_tags(self, filename: str) -> int:

        """Returns the number of tags matching the passed filename."""

        matching_tags = 0
        for tag in self.tags:
            if tag in filename.lower():
                matching_tags += 1

        return matching_tags

    def __repr__(self):
        return f"{self.path} <{self.tags}>"

    # Properties
    def to_JSON(self):

        """JSON serialization."""

        representation = {
            "tags": list(self.tags),
        }

        return representation
