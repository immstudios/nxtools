__all__ = ["PYTHON_VERSION", "NXTOOLS_VERSION"]

import sys

version_info = sys.version_info[:2]

PYTHON_VERSION = version_info[0] + float("." + str(version_info[1])) # TODO: make this nice
NXTOOLS_VERSION = 1.5

