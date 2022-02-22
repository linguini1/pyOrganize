# File system watch logic
__author__ = "Matteo Golin"

# Imports
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .manipulation import move_file
from .configure import LABELS


# Class to watch homed directory
class WatchDir:

    def __init__(self, config: dict):
        self.watchDir = config[LABELS["watchedDir"]]
        self.homeDir = config[LABELS["homeDir"]]
        self.config = config
        self.observer = Observer()

    def run(self, initial_sort):
        event_handler = Handler(self.config, debug=False)  # Custom event handler

        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()

        # Initial sort logic
        if initial_sort:
            for directory, _, files in os.walk(self.watchDir):
                for file in files:
                    move_file(f"{directory}/{file}", self.config)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Sorter terminated.")
        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, config: dict, debug=False):
        super(Handler, self).__init__()
        self.config = config
        self.debug = debug

    def on_any_event(self, event):

        """
        Creation events can be ignored, as they always trigger a modification event immediately afterwards, which is
        more important.
        """

        # Debugging
        if self.debug:
            print(event)

        # Move file to the directory it belongs in whenever a new file is detected
        if event.event_type in ["modified", "moved"] and not event.is_directory:

            time.sleep(1)  # Prevents error window in some cases

            # Get filepath
            if event.event_type == "modified":
                filepath = event.src_path.replace("\\", "/")
            else:
                filepath = event.dest_path.replace("\\", "/")

            move_file(filepath, self.config)  # Actually move the file
