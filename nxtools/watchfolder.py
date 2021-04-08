__all__ = ["WatchFolder"]

import os
import time

from .logging import logging, log_traceback
from .files import *

class WatchFolder():
    def __init__(self, input_dir, **kwargs):
        self.input_dir = input_dir
        self.settings = self.defaults
        self.settings.update(**kwargs)
        self.file_sizes = {}
        self.ignore_files = set()

    def __getitem__(self, key):
        return self.settings[key]

    @property
    def defaults(self):
        settings = {
            "iter_delay" : 20,
            "hidden" : False,
            "relative_path" : False,
            "case_sensitive_exts" : False,
            "use_file_sizes": True,
            "recursive" : True,
            "silent" : False,
            "exts" : []
        }
        return settings

    def start(self):
        while True:
            try:
                self.watch()
                self.clean_up()
                time.sleep(self.settings["iter_delay"])
            except KeyboardInterrupt:
                print ()
                logging.warning("User interrupt")
                break

    def clean_up(self):
        keys = [key for key in self.file_sizes.keys()]
        for file_path in keys:
            if not os.path.exists(file_path):
                del(self.file_sizes[file_path])
        keys = list(self.ignore_files)
        for key in keys:
            if not os.path.exists(key):
                self.ignore_files.remove(key)


    def watch(self):
        for input_path in get_files(
                    self.input_dir,
                    recursive=self.settings["recursive"],
                    hidden=self.settings["hidden"],
                    exts=self.settings["exts"],
                    relative_path=self.settings["relative_path"],
                    case_sensitive_exts=self.settings["case_sensitive_exts"]
                ):

            if self["relative_path"]:
                full_path = os.path.abspath(join_path(self.input_dir, input_path.path))
            else:
                full_path = os.path.abspath(input_path.path)

            if full_path in self.ignore_files:
                continue

            if not self["use_file_sizes"]:
                self.process(input_path)
                continue

            self.process_file_size = get_file_size(full_path)
            if self.process_file_size == 0:
                continue

            if not (full_path in self.file_sizes.keys() and self.file_sizes[full_path] == self.process_file_size):
                self.file_sizes[full_path] = self.process_file_size
                if not self.settings["silent"]:
                    logging.debug("Watching file {} ({} bytes)".format(input_path, input_path.size))
                continue
            if self.process(input_path):
                self.ignore_files.add(full_path)

    def process(self, input_path):
        pass

