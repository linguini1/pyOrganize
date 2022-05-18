# File system watch logic
__author__ = "Matteo Golin"

# Imports
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .application import Application


# Class to watch homed directory
class WatchDir:

    def __init__(self, app: Application):
        self.app = app
        self.observer = Observer()

    def run(self, initial_sort):
        event_handler = Handler(self.app, debug=False)  # Custom event handler

        self.observer.schedule(event_handler, self.app.config.watch_dir, recursive=True)
        self.observer.start()

        # Initial sort logic
        if initial_sort:
            for directory, _, files in os.walk(self.app.config.watch_dir):
                for file in files:
                    file_path = f"{self.app.config.watch_dir}\\{file}"
                    self.app.sort_file(file_path)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Sorter terminated.")
        finally:
            self.observer.join()
            self.app.clean_up()


class Handler(FileSystemEventHandler):

    def __init__(self, app: Application, debug=False):
        super(Handler, self).__init__()
        self.app = app
        self.debug = debug

    def on_any_event(self, event):

        """
        Creation events can be ignored, as they always trigger a modification event immediately afterwards, which is
        used as a signal.
        """

        # Debugging
        if self.debug:
            print(event)

        # Move file to the directory it belongs in whenever a new file is detected
        if event.event_type in ["modified", "moved"] and not event.is_directory:

            time.sleep(1)  # Prevents error window in some cases

            # Get filepath
            if event.event_type == "modified":
                file_path = event.src_path
            else:
                file_path = event.dest_path

            self.app.sort_file(file_path)

        elif event.event_type in ["modified", "moved"] and event.is_directory:
            pass  # TODO update directory path if an object is moved
