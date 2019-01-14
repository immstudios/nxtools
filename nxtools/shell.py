# The MIT License (MIT)
#
# Copyright (c) 2015 - 2017 imm studios, z.s.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import subprocess
import os
import uuid
import tempfile
import time

from .files import get_temp

__all__ = ["Shell"]

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
