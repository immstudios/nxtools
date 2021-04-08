from .version import *

if PYTHON_VERSION < 3.6:
    import sys
    print()
    print("CRITICAL ERROR: nxtools package requires Python version 3.6 or higher")
    sys.exit(1)

from .common import *
from .files import *
from .logging import *
from .text import *
from .shell import *
from .timeutils import *
from .watchfolder import *


