# Validators for command line input
__author__ = "Matteo Golin"

# Imports
import os

# Constants


# Filepath validator
def Directory(filepath: str) -> str:

    """Checks if the filepath given is a directory."""

    if os.path.isdir(filepath):
        return filepath
    else:
        raise NotADirectoryError("The given filepath does not point to a directory.")


def Char(character: str) -> str:

    """Ensure that string is only one character."""

    if len(character) == 1:
        return character

    else:
        raise ValueError("The ignore character must only be one character long.")
