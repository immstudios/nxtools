__all__ = [
        "FileObject",
        "join_path",
        "get_files",
        "get_path_pairs",
        "get_temp",
        "get_base_name",
        "file_to_title",
        "get_file_siblings",
    ]

import os
import tempfile
import stat
import uuid
import time

from .common import get_guid
from .logging import logging, log_traceback
from .text import slugify


class FileObject(object):
    def __init__(self, *args, **kwargs):
        self.path = os.path.join(*args)
        self.attrs = {}

    def __str__(self):
        return self.path

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def load_stat(self):
        stat_result = os.stat(self.path)
        self.attrs.update({
                "mode" : stat_result[stat.ST_MODE],
                "ino" : stat_result[stat.ST_INO],
                "uid" : stat_result[stat.ST_UID],
                "gid" : stat_result[stat.ST_GID],
                "size" : stat_result[stat.ST_SIZE],
                "atime" : stat_result[stat.ST_ATIME],
                "mtime" : stat_result[stat.ST_MTIME],
                "ctime" : stat_result[stat.ST_CTIME]
            })

    @property
    def atime(self):
        if not "atime" in self.attrs:
            self.load_stat()
        return self["atime"]

    @property
    def ctime(self):
        if not "ctime" in self.attrs:
            self.load_stat()
        return self["ctime"]

    @property
    def mtime(self):
        if not "mtime" in self.attrs:
            self.load_stat()
        return self["mtime"]

    @property
    def size(self):
        if not "size" in self.attrs:
            self.load_stat()
        return self["size"]

    @property
    def is_dir(self):
        if not "mode" in self.attrs:
            self.load_stat()
        return stat.S_ISDIR(self["mode"])

    @property
    def is_reg(self):
        if not "mode" in self.attrs:
            self.load_stat()
        return stat.S_ISREG(self["mode"])

    @property
    def is_file(self):
        return os.path.isfile(self.path)

    @property
    def is_link(self):
        if not "mode" in self.attrs:
            self.load_stat()
        return stat.S_ISLNK(self["mode"])

    @property
    def is_fifo(self):
        if not "mode" in self.attrs:
            self.load_stat()
        return stat.S_ISFIFO(self["mode"])

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def ext(self):
        return os.path.splitext(self.path)[1].lstrip(".")

    @property
    def dir_name(self):
        return os.path.split(self.path)[0]

    @property
    def base_name(self):
        return os.path.splitext(os.path.basename(self.path))[0]

    def open(self, mode="r", **kwargs):
        return open(self.path, mode, **kwargs)


def join_path(*args):
    elms = []
    for arg in args:
        if isinstance(arg, FileObject):
            elms.append(arg.path)
        else:
            elms.append(arg)
    return os.path.join(*elms)


def get_files(
        base_path:str,
        recursive:bool=False,
        hidden:bool=False,
        exts:list=[],
        case_sensitive_exts:bool=False,
        relative_path:bool=False,
        strip_path:str=None,
    ):
    """Crawls a given directory (base_path) and yields a FileObject object for each file found.

    Since scandir is used for crawling, file attributes (ctime, mtime, size...) are instantly available.

    Args:
        base_path (str): Path to the directory to be crawled
        recursive (bool): Crawl recursively (default: False)
        hidden (bool): Yield hidden (dot)files too (default: False)
        exts (list): If specified, yields only files matching given extensions
        case_sensitive_exts (bool): Do not ignore cases when `exts` list is used (default: False)
    """

    if not case_sensitive_exts:
        exts = [ext.lower() for ext in exts]

    if strip_path is None:
        strip_path = base_path

    if os.path.exists(base_path):
        for dir_entry in os.scandir(base_path):
            file_name = dir_entry.name
            file_path = dir_entry.path
            stat_result = dir_entry.stat()

            file_object = FileObject(
                    file_path,
                    mode=stat_result[stat.ST_MODE],
                    ino=stat_result[stat.ST_INO],
                    uid=stat_result[stat.ST_UID],
                    gid=stat_result[stat.ST_GID],
                    size=stat_result[stat.ST_SIZE],
                    atime=stat_result[stat.ST_ATIME],
                    mtime=stat_result[stat.ST_MTIME],
                    ctime=stat_result[stat.ST_CTIME]
                )

            if not hidden and file_name.startswith("."):
                continue

            if file_object.is_reg:
                ext = os.path.splitext(file_name)[1].lstrip(".")
                if not case_sensitive_exts:
                    ext = ext.lower()
                if exts and ext not in exts:
                    continue
                if relative_path:
                    file_object.path = file_object.path.replace(strip_path, "", 1).lstrip(os.path.sep)
                    yield file_object
                else:
                    yield file_object
            elif file_object.is_dir and recursive:
                for file_object in get_files(
                            file_object.path,
                            recursive=recursive,
                            hidden=hidden,
                            case_sensitive_exts=case_sensitive_exts,
                            exts=exts,
                            relative_path=relative_path,
                            strip_path=strip_path
                        ):
                    yield file_object


def get_path_pairs(input_dir, output_dir, **kwargs):
    """Crawls input_dir using get_files and yields tuples of input and output files.

    This function is useful for batch conversion, when you need to process files
    from `input_dir` and output the result to a `output_dir`.

    Most arguments are the same as for `get_files`. You can also specify a target extension,
    use a slugifier for the output path.

    Args:
        target_ext (str):
        target_slugify (bool): (default: False)
    """
    kwargs["relative_path"] = True
    kwargs["recursive"] = True
    target_ext = kwargs.get("target_ext", False)

    for input_file in get_files(input_dir, **kwargs):
        input_path = input_file.path.replace("\\", "/")
        if kwargs.get("target_slugify", False):
            output_path = join_path(
                    output_dir,
                    *[slugify(f) for f in input_file.dir_name.split("/")] +
                    [slugify(input_file.base_name)]
                )
            if input_file.ext:
                output_path += "." + input_file.ext
        else:
            output_path = join_path(output_dir, input_file.path)

        input_file = FileObject(input_dir, input_path)
        output_file = FileObject(output_path)

        if target_ext:
            output_file.path = os.path.splitext(output_file.path)[0] + "." + target_ext
        yield input_file, output_file


def get_temp(extension=False, root=False):
    """Returns a path to a temporary file

    Args:
        extension (str)
        root (str)
    """
    if not root:
        root = tempfile.gettempdir()
    filename = join_path(root, get_guid())
    if extension:
        filename = filename + "." + extension
    return filename


def get_base_name(fname):
    """Strips a directory and and extension from a given path.

    `/etc/foo/bar.baz` becomes `bar`

    Args:
        fname (str): path-like object, string or FileObject

    Returns:
        str
    """
    return os.path.splitext(os.path.basename(str(fname)))[0]


def file_to_title(fname):
    base = get_base_name(fname)
    base = base.replace("_"," ").replace("-"," - ").strip()
    elms = []
    capd = False
    for i, elm in enumerate(base.split(" ")):
        if not elm:
            continue
        if not capd and not (elm.isdigit() or elm.upper()==elm):
            elm = elm.capitalize()
            capd = True
        elms.append(elm)
    return " ".join(elms)


def get_file_siblings(path, exts=[]):
    #TODO: Rewrite this
    root = os.path.splitext(path)[0]
    for f in exts:
        tstf = root + "." + f
        if os.path.exists(tstf):
            yield tstf


def get_file_size(path):
    try:
        f = open(str(path), "rb")
    except Exception:
        log_traceback(f"Exception! File {path} is not accessible")
        return 0
    f.seek(0, 2)
    return f.tell()

