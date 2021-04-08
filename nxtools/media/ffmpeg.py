__all__ = ["FFMPEG", "ffmpeg", "enable_ffmpeg_debug"]

import os
import re
import time
import subprocess
import copy
import signal

from nxtools.logging import *
from nxtools.text import indent


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
        self.cmd.extend(str(arg) for arg in args)

    def reset_stderr(self):
        self.buff = b""
        self.error_log = ""

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
        self.error_log += self.stderr.read().decode("utf-8")
        if interrupted:
            raise KeyboardInterrupt


    def process(self, progress_handler=None):
        ch = self.proc.stderr.read(1)
        if not ch:
            return False
        if ch in [b"\n", b"\r"]:
            if progress_handler:
                position_match = re_position.search(self.buff.decode("utf-8"))
                if position_match:
                    position = time2sec(position_match)
                    progress_handler(position)
            else:
                try:
                    self.error_log += self.buff.decode("utf-8") + "\n"
                except Exception:
                    pass
            if FFMPEG_DEBUG:
                print (self.buff.rstrip())
            self.buff = b""
        else:
            self.buff += ch
        return True



def ffmpeg(*args, **kwargs):
    """Universal ffmpeg wrapper with progress and error handling"""

    ff = FFMPEG(*args, **kwargs)
    ff.start(
            stdin=kwargs.get("stdin", subprocess.PIPE),
            stdout=kwargs.get("stdout", None),
            stderr=kwargs.get("stderr", subprocess.PIPE)
        )

    ff.wait(kwargs.get("progress_handler", None))

    if ff.return_code:
        err = indent(ff.error_log)
        logging.error("Problem occured during transcoding\n\n{}\n\n".format(err))
        return False
    return True
