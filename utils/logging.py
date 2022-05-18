# Logging information to console and to a log file so that files aren't lost if they're moved unexpectedly
__author__ = "Matteo Golin"

# Imports

# Constants
LOG_FILE = "log.txt"


# Functions
def write_to_log(info: str):

    """Writes information to the logging file."""

    with open(LOG_FILE, "a") as log:
        log.write(f"{info}\n")


def log_file_movement(old_path: str, new_path: str):

    """Logs the movement of a file."""

    file_name = old_path.split("\\")[-1]

    info = f"{file_name} was moved from {old_path.replace(file_name, '')} to {new_path.replace(file_name, '')}"
    print(info)
    write_to_log(info)
