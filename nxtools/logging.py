__all__ = [
        "Logging",
        "logging",
        "log_traceback",
        "critical_error",
        "log_to_file"
    ]

import os
import sys
import time
import traceback
import functools

from .common import PLATFORM
from .text import indent
from .timeutils import format_time

DEBUG, INFO, WARNING, ERROR, GOOD_NEWS = range(5)


# Log handlers

def null_handler(**kwargs):
    return True


def log_to_file(log_path):
    def log_to_file_handler(path, **kwargs):
        placeholders = {
            "date" : format_time(time.time(), "%Y-%m-%d")
        }
        path = path.format(**placeholders)
        dirname, fname = os.path.split(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(path, "a") as f:
            tstamp = format_time(time.time())
            ltype = {
                   0 : "DEBUG    ",
                   1 : "INFO     ",
                   2 : "WARNING  ",
                   3 : "ERROR    ",
                   4 : "GOOD NEWS"
                }[kwargs["message_type"]]
            f.write("{}  {}  {}\n".format(tstamp, ltype, kwargs["message"]))

    return functools.partial(log_to_file_handler, log_path)


# Logging

class Logging():
    """
    nxtools universal logger
    """
    def __init__(self, user=""):
        self.show_time = False
        self.show_colors = True
        self.user = user
        self.handlers = []
        self.file = sys.stderr
        self.formats = {
            INFO      : "{2}INFO       {0} {1}",
            DEBUG     : "{2}\033[34mDEBUG      {0} {1}\033[0m",
            WARNING   : "{2}\033[33mWARNING\033[0m    {0} {1}",
            ERROR     : "{2}\033[31mERROR\033[0m      {0} {1}",
            GOOD_NEWS : "{2}\033[32mGOOD NEWS\033[0m  {0} {1}"
            }

        self.formats_nocolor = {
            DEBUG     : "{2}DEBUG     {0} {1}",
            INFO      : "{2}INFO      {0} {1}",
            WARNING   : "{2}WARNING   {0} {1}",
            ERROR     : "{2}ERROR     {0} {1}",
            GOOD_NEWS : "{2}GOOD NEWS {0} {1}"
            }

    def add_handler(self, handler):
        if not handler in self.handlers:
            self.handlers.append(handler)

    def _send(self, msgtype, *args, **kwargs):
        message = " ".join([str(arg) for arg in args])
        user = kwargs.get("user", self.user)
        timestamp = format_time(time.time()) + " " if self.show_time else ""
        if user:
            user = " {:<15}".format(user)
        if kwargs.get("handlers", True):
            for handler in self.handlers:
                handler(user=self.user, message_type=msgtype, message=message)

        colors = self.show_colors and PLATFORM == "unix"
        if colors:
            if timestamp:
                timestamp = "\033[1;30m{}\033[0m".format(timestamp)
            try:
                print(self.formats[msgtype].format(user, message, timestamp), file=self.file)
            except Exception:
                pass
        else:
            try:
                print(self.formats_nocolor[msgtype].format(user, message, timestamp), file=self.file)
            except Exception:
                pass

    def debug(self, *args, **kwargs):
        """Log debug message"""
        self._send(DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        """Log info message"""
        self._send(INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """Log warning message"""
        self._send(WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        """Log error message"""
        self._send(ERROR, *args, **kwargs)

    def goodnews(self, *args, **kwargs):
        """Log good news"""
        self._send(GOOD_NEWS, *args, **kwargs)

logging = Logging()


def log_traceback(message="Exception!", **kwargs):
    """
    Show current exception in log
    """
    tb = traceback.format_exc()
    msg = "{}\n\n{}".format(message, indent(tb))
    logging.error(msg, **kwargs)
    return msg


def critical_error(msg, **kwargs):
    """
    sys exit
    """
    logging.error(msg, **kwargs)
    logging.debug("Critical error. Terminating program.")
    sys.exit(1)
