# The MIT License (MIT)
#
# Copyright (c) 2015 - 2018 imm studios, z.s.
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
import json
import subprocess
import signal

from nxtools.common import decode_if_py3, string_types
from nxtools.text import indent
from nxtools.logging import *
from nxtools.files import FileObject

__all__ = ["ffprobe"]

def ffprobe(input_file, verbose=False):
    """Runs ffprobe on file and returns python dict with result"""
    if isinstance(input_file, FileObject):
        exists = input_file.exists
        path = input_file.path
    elif type(input_file) in string_types:
        exists = os.path.exists(input_file)
        path = input_file
    else:
        raise TypeError("input_path must be of string or FileObject type")
    if not exists:
        logging.error("ffprobe: file does not exist ({})".format(input_file))
        return False
    cmd = [
            "ffprobe",
            "-show_format",
            "-show_streams",
            "-print_format", "json",
            path
        ]
    FNULL = open(os.devnull, "w")
    if verbose:
        logging.debug("Executing {}".format(" ".join(cmd)))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = decode_if_py3(proc.stdout.read())
    proc.wait()
    if proc.returncode:
        if verbose:
            logging.error("Unable to read media file {}\n\n{}\n\n".format(input_file, indent(proc.stderr.read())))
        else:
            logging.warning("Unable to read media file {}".format(input_file))
        return False
    return json.loads(res)
