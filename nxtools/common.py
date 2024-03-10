import os
import sys
import uuid
from typing import Literal
from xml.etree import ElementTree

from .logging import logging

PLATFORM = "windows" if sys.platform == "win32" else "unix"


def xml(data: str) -> ElementTree.Element | None:
    """Parse an XML string using ElementTree

    Args:
        data (str): The XML document to parse

    Returns:
        ElementTree.Element: The root element of the parsed XML string
    """
    return ElementTree.XML(data)


def get_uuid(uuid_type: Literal[1, 4] = 1) -> str:
    """Return an UUID of the specified type"""
    if uuid_type == 1:
        return str(uuid.uuid1())
    elif uuid_type == 4:
        return str(uuid.uuid4())


def get_guid() -> str:
    """Return a GUID"""
    logging.warning("get_guid() is deprecated, use get_uuid(4) instead")
    return get_uuid(4).upper()


def find_binary(file_name: str) -> str | None:
    """Attempt to find a given executable and return its path

    Args:
        file_name (str): The name of the executable to find

    Returns:
        str: The path to the executable
    """
    if PLATFORM == "unix":
        if os.path.exists(file_name) and file_name == os.path.basename(file_name):
            return "./" + file_name
        return file_name
    elif PLATFORM == "windows":
        if not file_name.endswith(".exe"):
            file_name = file_name + ".exe"
        for path in sys.path:
            fpath = os.path.join(path, file_name)
            if os.path.exists(fpath):
                return fpath
    raise FileNotFoundError(f"Could not find {file_name}")
