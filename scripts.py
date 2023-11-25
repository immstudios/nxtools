import subprocess
import textwrap

import nxtools

DOC_IGNORE = """
__builtins__
__cached__
__doc__
__file__
__loader__
__name__
__package__
__path__
__spec__

EMAIL_REGEXP
GUID_REGEXP
NXTOOLS_VERSION

PLATFORM

string_type
string_types

watchfolder
Logging
common
files
logging
shell
text
timeutils
"""

DOC_TPL = """nxtools
=======

nxtools is a set of various tools and helpers used by [Nebula](https://github.com/nebulabroadcast/nebula) and other software.

Installation
------------

`pip install nxtools`

### Optional dependencies

 - `unidecode` for full unicode transliteration
 - `colorama` for colored log output even on Windows


Examples
-------

 - [Podcasts downloader](https://pastebin.com/5Fya2kep)

Reference
---------

"""


def test():
    subprocess.run(
        ['python', '-u', '-m', 'unittest', 'discover']
    )


def docs():
    ignore = [i.strip() for i in DOC_IGNORE.split("\n") if i.strip()]
    result = DOC_TPL
    for name in dir(nxtools):
        if name in ignore:
            continue

        obj = getattr(nxtools, name)

        doc = obj.__doc__
        if doc is None:
            continue

        doc = doc.strip()

        doclines = doc.split("\n")
        summary = doclines[0].strip()
        doclines.pop(0)
        description = ""

        while doclines:
            line = doclines[0].strip()
            if line.strip().startswith("Args"):
                break
            description += line.strip() + "\n"
            doclines.pop(0)

        result += f"\n### {name}\n\n{summary}\n"
        if description.strip():
            result += description.rstrip()

        if doclines:
            result += "\n\n```\n"
            result += textwrap.dedent("\n".join(doclines))
            result += "\n```\n"

    with open("README.md","w") as f:
        f.write(result)

