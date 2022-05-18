# Basic utility functions
__author__ = "Matteo Golin"

# Imports

# Constants


# Functions
def filename(file_path: str) -> str:

    """Returns the filename separated from the file path."""

    return file_path.split("\\")[-1]

