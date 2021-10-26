import unittest

from nxtools import *

class TestJoinPath(unittest.TestCase):
    def test_strings(self):
        result = join_path("/usr", "bin", "env")
        assert result == "/usr/bin/env"


class TestGetFiles(unittest.TestCase):
    def test_attrs(self):
        for f in get_files("nxtools", recursive=True):
            assert type(f.size) == int

