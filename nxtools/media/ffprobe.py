__all__ = ["ffprobe"]

import os
import json
import subprocess

from nxtools.text import indent
from nxtools.logging import *
from nxtools.files import FileObject


def ffprobe(input_file, verbose=False):
    """Runs ffprobe on file and returns python dict with result"""
    if isinstance(input_file, FileObject):
        exists = input_file.exists
        path = input_file.path
    elif type(input_file) == str:
        exists = os.path.exists(input_file)
        path = input_file
    else:
        raise TypeError("input_path must be of string or FileObject type")
    if not exists:
        logging.error(f"ffprobe: file '{input_file}' does not exist")
        return {}
    cmd = [
        "ffprobe",
        "-show_format",
        "-show_streams",
        "-print_format", "json",
        path
    ]
    FNULL = open(os.devnull, "w")
    if verbose:
        logging.debug(f"Executing {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = proc.stdout.read().decode("utf-8")
    proc.wait()
    if proc.returncode:
        if verbose:
            error_msg = indent(proc.stderr.read())
            logging.error(f"Unable to read media file {input_file}\n\n{error_msg}\n\n")
        else:
            logging.warning(f"Unable to read media file {input_file}")
        return False
    return json.loads(res)
