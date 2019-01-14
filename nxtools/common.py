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

import os
import sys
import uuid

from xml.etree import ElementTree as ET

__all__ = ["decode_if_py3", "encode_if_py3", "PLATFORM", "PYTHON_VERSION", "find_binary", "get_guid", "xml", "string_type", "string_types"]

version_info = sys.version_info[:2]
PYTHON_VERSION = version_info[0] + float("." + str(version_info[1])) # TODO: make this nice

if PYTHON_VERSION >= 3:
    decode_if_py3 = lambda x, enc="utf-8": x.decode(enc)
    encode_if_py3 = lambda x, enc="utf-8": bytes(x, enc) if type(x) == str else x
    string_type = str
    string_types = [str]
else:
    decode_if_py3 = lambda x: x
    encode_if_py3 = lambda x: x
    string_type = unicode
    string_types = [str, unicode]

PLATFORM = "windows" if sys.platform == "win32" else "unix"

def xml(data):
    return ET.XML(data)

def get_guid():
    return str(uuid.uuid1())

def find_binary(fname):
    if PLATFORM == "unix":
        if os.path.exists(fname) and fname == os.path.basename(fname):
            return "./" + fname
        return fname
    elif PLATFORM == "windows":
        if not fname.endswith(".exe"):
            fname = fname + ".exe"
        for path in sys.path:
            fpath = os.path.join(path, fname)
            if os.path.exists(fpath):
                return fpath
