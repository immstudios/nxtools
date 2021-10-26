import unittest

from nxtools import *


class TestGetFiles(unittest.TestCase):
    def test_colors(self):
        print ()
        logging.debug("This is a debug message")
        logging.info("This is an info message")
        logging.warning("This is a warning message")
        logging.error("This is a error message")
        logging.goodnews("This is a good news message")


        try:
            i = 1/0
        except Exception:
            log_traceback("This is a handled exception")

        try:
            critical_error("This is very bad")
        except SystemExit:
            logging.goodnews("Actually good")
