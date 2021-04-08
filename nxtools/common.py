__all__ = [
        "decode_if_py3",
        "encode_if_py3",
        "PLATFORM",
        "find_binary",
        "get_guid",
        "xml",
        "string_type",
        "string_types"
    ]

import os
import sys
import uuid

from xml.etree import ElementTree as ET

# DEPRECATED
decode_if_py3 = lambda x, enc="utf-8": x.decode(enc)
encode_if_py3 = lambda x, enc="utf-8": bytes(x, enc) if type(x) == str else x
string_type = str
string_types = [str]

PLATFORM = "windows" if sys.platform == "win32" else "unix"

def xml(data):
    """Parse an XML using ElementTree"""
    return ET.XML(data)

def get_guid():
    """Returns a GUID :)"""
    return str(uuid.uuid1())

def find_binary(fname):
    """Attempt to find a given executable and return its path
    """
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
