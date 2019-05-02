__all__ = ["Shell"]

import subprocess
import os
import uuid
import tempfile
import time

from .files import get_temp

class Shell():
    def __init__(self, cmd):
        """Believe or not, using temp files is much more stable than subprocess library. Especially on windows."""
        self.out_fn = get_temp()
        self.err_fn = get_temp()
        self.retcode = self._exec("%s > %s 2> %s" % (cmd, self.out_fn, self.err_fn))

    def _exec(self, cmd):
        proc = subprocess.Popen(cmd, shell=True)
        while proc.poll() == None:
            time.sleep(.1)
        return proc.poll()

    def stdout(self):
        return open(self.out_fn)

    def stderr(self):
        return open(self.err_fn)
