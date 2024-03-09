import contextlib
import logging as _logging
import sys
import time
import traceback

import colorama

from .text import indent
from .timeutils import format_time

colorama.init()

SBB = colorama.Style.BRIGHT + colorama.Fore.BLACK
SR = colorama.Style.RESET_ALL
SN = colorama.Style.NORMAL

TRACE = 0
DEBUG = 10
INFO = 20
GOOD_NEWS = 25
WARNING = 30
ERROR = 40
CRITICAL = 50

LEVEL_WIDTH = 10

FMT_COLORAMA = {
    TRACE: SBB
    + "{timestamp}"
    + "TRACE".ljust(LEVEL_WIDTH)
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    DEBUG: SBB
    + "{timestamp}"
    + colorama.Style.RESET_ALL
    + colorama.Fore.BLUE
    + "DEBUG".ljust(LEVEL_WIDTH)
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    INFO: SBB
    + "{timestamp}"
    + colorama.Style.NORMAL
    + colorama.Fore.WHITE
    + "INFO ".ljust(LEVEL_WIDTH)
    + colorama.Fore.RESET
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    WARNING: SBB
    + "{timestamp}"
    + colorama.Style.NORMAL
    + colorama.Fore.YELLOW
    + "WARNING ".ljust(LEVEL_WIDTH)
    + colorama.Fore.RESET
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    ERROR: SBB
    + "{timestamp}"
    + colorama.Style.NORMAL
    + colorama.Fore.RED
    + "ERROR".ljust(LEVEL_WIDTH)
    + colorama.Fore.RESET
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    CRITICAL: SBB
    + "{timestamp}"
    + colorama.Style.NORMAL
    + colorama.Fore.RED
    + "CRITICAL ".ljust(LEVEL_WIDTH)
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
    GOOD_NEWS: SBB
    + "{timestamp}"
    + colorama.Style.NORMAL
    + colorama.Fore.GREEN
    + "GOOD NEWS ".ljust(LEVEL_WIDTH)
    + colorama.Fore.RESET
    + "{user} {message}"
    + colorama.Style.RESET_ALL,
}


class Logging:
    """nxtools universal logger."""

    user: str | None = None
    show_user: bool = True
    show_time: bool = True

    def __init__(self):
        self.show_time = True
        self.show_colors = True
        self.handlers = []

    def install(self):
        """Use this logger as the default logger.

        This method installs the logger as the default logger
        for the standard logging module. It unifies the logging
        format, colorizes the output and adds a custom handler
        support.
        """
        logger = _logging.getLogger()
        logger.setLevel(DEBUG)

        printer = self._send

        class CustomHandler(_logging.Handler):
            def emit(self, record):
                log_message = self.format(record)
                name = record.name
                printer(record.levelno, log_message, user=name)

        logger.addHandler(CustomHandler())

    def add_handler(self, handler):
        """Add a new logging handler."""
        if handler not in self.handlers:
            self.handlers.append(handler)

    def _send(self, level, *args, **kwargs):
        message = " ".join([str(arg) for arg in args])
        user = kwargs.get("user", self.user)

        if user is None or not self.show_user:
            user = ""
        else:
            user = f"{user:<15}"

        if self.show_time:
            timestamp = format_time(time.time()) + " "
        else:
            timestamp = ""

        line = FMT_COLORAMA[level].format(
            timestamp=timestamp,
            user=user,
            message=message,
        )

        with contextlib.suppress(Exception):
            print(line, file=sys.stderr)

        if kwargs.get("handlers", True):
            for handler in self.handlers:
                handler(user=self.user, message_type=level, message=message)

    def trace(self, *args, **kwargs):
        """Log a debug message."""
        self._send(TRACE, *args, **kwargs)

    def debug(self, *args, **kwargs):
        """Log a debug message."""
        self._send(DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        """Log an info message."""
        self._send(INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """Log a warning message."""
        self._send(WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        """Log an error message."""
        self._send(ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        """Log a critical error message."""
        self._send(CRITICAL, *args, **kwargs)

    def goodnews(self, *args, **kwargs):
        """Log a good news message."""
        self._send(GOOD_NEWS, *args, **kwargs)


def log_traceback(message="Exception!", **kwargs):
    """Log the current exception traceback."""
    tb = traceback.format_exc()
    msg = f"{message}\n\n{indent(tb)}"
    logging.error(msg, **kwargs)
    return msg


def critical_error(message, return_code=1, **kwargs):
    """Log an error message and exit program."""
    logging.error(message, **kwargs)
    logging.debug("Critical error. Terminating program.")
    sys.exit(return_code)


logging = Logging()
