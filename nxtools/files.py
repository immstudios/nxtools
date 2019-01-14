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
import tempfile
import stat
import uuid
import time

from .logging import *
from .misc import slugify
from .common import PYTHON_VERSION, get_guid

__all__ = [
        "FileObject",
        "join_path",
        "get_files",
        "get_path_pairs",
        "get_temp",
        "get_base_name",
        "file_to_title",
        "get_file_siblings",
        "WatchFolder"
    ]


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


def get_files(base_path, **kwargs):
    if PYTHON_VERSION >= 3.5:
        list_func = os.scandir
    else:
        list_func = os.listdir

    recursive = kwargs.get("recursive", False)
    hidden = kwargs.get("hidden", False)
    relative_path = kwargs.get("relative_path", False)
    case_sensitive_exts = kwargs.get("case_sensitive_exts", False)
    if case_sensitive_exts:
        exts = kwargs.get("exts", [])
    else:
        exts = [ext.lower() for ext in kwargs.get("exts", [])]
    strip_path = kwargs.get("strip_path", base_path)
    if os.path.exists(base_path):
        for dir_entry in list_func(base_path):

            if PYTHON_VERSION >= 3:
                file_name = dir_entry.name
                file_path = dir_entry.path
                stat_result = dir_entry.stat()
            else:
                file_name = dir_entry
                file_path = join_path(base_path, dir_entry)
                stat_result = os.stat(file_path)

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
    if not root:
        root = tempfile.gettempdir()
    filename = join_path(root, get_guid())
    if extension:
        filename = filename + "." + extension
    return filename


def get_base_name(fname):
    return os.path.splitext(os.path.basename(fname))[0]


def file_to_title(fname):
    base = get_base_name(fname)
    base = base.replace("_"," ").replace("-"," - ").strip()
    elms = []
    capd = False
    for i, elm in enumerate(base.split(" ")):
        if not elm: continue
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
        log_traceback("Exception! File {} is not accessible".format(path))
        return 0
    f.seek(0, 2)
    return f.tell()


class WatchFolder():
    def __init__(self, input_dir, **kwargs):
        self.input_dir = input_dir
        self.settings = self.defaults
        self.settings.update(**kwargs)
        self.file_sizes = {}
        if "valid_exts" in kwargs:
            logging.warning("Watchfolder: valid_exts is deprecated. Use exts instead")
            self.settings["exts"] = kwargs["valid_exts"]
        self.ignore_files = set()

    def __getitem__(self, key):
        return self.settings[key]

    @property
    def defaults(self):
        settings = {
            "iter_delay" : 20,
            "hidden" : False,
            "relative_path" : False,
            "case_sensitive_exts" : False,
            "use_file_sizes": True,
            "recursive" : True,
            "silent" : False,
            "exts" : []
            }
        return settings

    def start(self):
        while True:
            try:
                self.watch()
                self.clean_up()
                time.sleep(self.settings["iter_delay"])
            except KeyboardInterrupt:
                print ()
                logging.warning("User interrupt")
                break

    def clean_up(self):
        keys = [key for key in self.file_sizes.keys()]
        for file_path in keys:
            if not os.path.exists(file_path):
                del(self.file_sizes[file_path])
        keys = list(self.ignore_files)
        for key in keys:
            if not os.path.exists(key):
                self.ignore_files.remove(key)


    def watch(self):
        for input_path in get_files(
                    self.input_dir,
                    recursive=self.settings["recursive"],
                    hidden=self.settings["hidden"],
                    exts=self.settings["exts"],
                    relative_path=self.settings["relative_path"],
                    case_sensitive_exts=self.settings["case_sensitive_exts"]
                ):

            if self["relative_path"]:
                full_path = os.path.abspath(join_path(self.input_dir, input_path.path))
            else:
                full_path = os.path.abspath(input_path.path)

            if full_path in self.ignore_files:
                continue

            if not self["use_file_sizes"]:
                self.process(input_path)
                continue

            self.process_file_size = get_file_size(full_path)
            if self.process_file_size == 0:
                continue

            if not (full_path in self.file_sizes.keys() and self.file_sizes[full_path] == self.process_file_size):
                self.file_sizes[full_path] = self.process_file_size
                if not self.settings["silent"]:
                    logging.debug("Watching file {} ({} bytes)".format(input_path, input_path.size))
                continue
            if self.process(input_path):
                self.ignore_files.add(full_path)

    def process(self, input_path):
        pass
