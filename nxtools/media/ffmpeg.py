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

from __future__ import print_function

import os
import re
import time
import subprocess
import copy
import signal

from nxtools.logging import *
from nxtools.common import decode_if_py3, PYTHON_VERSION
from nxtools.text import indent

__all__ = ["enable_ffmpeg_debug", "FFMPEG", "ffmpeg"]

FFMPEG_DEBUG = False

re_position = re.compile('time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})\d*', re.U | re.I)

def enable_ffmpeg_debug():
    global FFMPEG_DEBUG
    FFMPEG_DEBUG = True

def time2sec(search):
    hh, mm, ss, cs =  search.group(1), search.group(2), search.group(3), search.group(4)
    return int(hh)*3600 + int(mm)*60 + int(ss) + int(cs)/100.0
    return sum([i**(2-i) * int(search.group(i+1)) for i in range(3)])

class FFMPEG():
    def __init__(self, *args, **kwargs):
        if kwargs.get("debug", False):
            enable_ffmpeg_debug()
        if FFMPEG_DEBUG:
            logging.warning("FFMPEG debug mode is enabled")

        self.proc = None
        self.cmd = ["ffmpeg", "-hide_banner"]

        if len(args) == 2 and "output_format" in kwargs:
            input_path, output_path = [str(arg) for arg in args]
            input_format = kwargs.get("input_format", [])
            output_format = kwargs.get("output_format", [])

            self.cmd.append("-y")
            for p in input_format:
                self.cmd.extend(self.make_profile(p))
            self.cmd.extend(["-i", input_path])
            for p in output_format:
                self.cmd.extend(self.make_profile(p))
            self.cmd.append(output_path)
            self.reset_stderr()
        else:
            self.cmd.extend(str(arg) for arg in args)

    def reset_stderr(self):
        if PYTHON_VERSION < 3:
            self.buff = ""
        else:
            self.buff = b""
        self.error_log = ""


    @staticmethod
    def make_profile(p):
        cmd = []
        if type(p) == list and len(p) == 2:
            key, val = p
        elif type(p) == list:
            key = p[0]
            val = False
        else:
            key = p
            val = False
        cmd.append("-" + str(key))
        if val:
            cmd.append(str(val))
        return cmd

    @property
    def is_running(self):
        return bool(self.proc) and self.proc.poll() == None

    @property
    def stdin(self):
        return self.proc.stdin

    @property
    def stdout(self):
        return self.proc.stdout

    @property
    def stderr(self):
        return self.proc.stderr

    @property
    def return_code(self):
        return self.proc.returncode

    def start(self, stdin=None, stdout=None, stderr=subprocess.PIPE):
        self.reset_stderr()
        logging.debug("Executing", " ".join(self.cmd))
        self.proc = subprocess.Popen(
                self.cmd,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
            )

    def stop(self):
        if not self.proc:
            return False
        self.proc.send_signal(signal.SIGINT)
        return True

    def wait(self, progress_handler=None):
        interrupted = False
        try:
            while True:
                if not self.process(progress_handler=progress_handler):
                    break
        except KeyboardInterrupt:
            self.stop()
            interrupted = True
        self.proc.wait()
        self.error_log += decode_if_py3(self.stderr.read())
        if interrupted:
            raise KeyboardInterrupt


    def process(self, progress_handler=None):
        ch = self.proc.stderr.read(1)
        if not ch:
            return False
        if ch in ["\n", "\r", b"\n", b"\r"]:
            if progress_handler:
                position_match = re_position.search(decode_if_py3(self.buff))
                if position_match:
                    position = time2sec(position_match)
                    progress_handler(position)
            else:
                try:
                    self.error_log += decode_if_py3(self.buff) + "\n"
                except:
                    pass
            if FFMPEG_DEBUG:
                print (self.buff.rstrip())
            if PYTHON_VERSION < 3:
                self.buff = ""
            else:
                self.buff = b""
        else:
            self.buff += ch
        return True



def ffmpeg(*args, **kwargs):
    """Universal ffmpeg wrapper with progress and error handling"""

    ff = FFMPEG(*args, **kwargs)
    ff.start(
            stdin=kwargs.get("stdin", None),
            stdout=kwargs.get("stdout", None),
            stderr=kwargs.get("stderr", subprocess.PIPE)
        )

    ff.wait(kwargs.get("progress_handler", None))

    if ff.return_code:
        err = indent(ff.error_log)
        logging.error("Problem occured during transcoding\n\n{}\n\n".format(err))
        return False
    return True
