__all__ = [
        "to_unicode",
        "indent",
        "unaccent",
        "slugify",
        "string2color",
        "fract2float",
        "format_filesize",
        "EMAIL_REGEXP",
        "GUID_REGEXP"
    ]


import string

from .common import *

try:
    import unidecode
    has_unidecode = True
except ImportError:
    has_unidecode = False
    if PYTHON_VERSION < 3:
        import unicodedata


#: E-mail address regular expression
EMAIL_REGEXP = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#: GUID/UUID regular expression
GUID_REGEXP = r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"


if PYTHON_VERSION < 3:
    default_slug_whitelist = string.letters + string.digits
else:
    default_slug_whitelist = string.ascii_letters + string.digits
slug_separator_whitelist = " ,./\\;:!|*^#@~+-_="


def indent(src, l=4):
    """
    Indent given text
    """
    return "\n".join(["{}{}".format(l*" ", s.rstrip()) for s in src.split("\n")]) + "\n" if src.endswith("\n") else ""

def to_unicode(string, encoding="utf-8"):
    if PYTHON_VERSION < 3:
        if type(string) == str:
            string = unicode(string, encoding)
    return string

def unaccent(string, encoding="utf-8"):
    """not just unaccent, but full to-ascii transliteration"""
    string = to_unicode(string)
    if has_unidecode:
        return unidecode.unidecode(string)
    if PYTHON_VERSION < 3:
        if type(string) == str:
            string = unicode(string, encoding)
        nfkd_form = unicodedata.normalize('NFKD', string)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).encode("ascii", "ignore")
    else:
        return string #TODO

def slugify(input_string, **kwargs):
    """
    Slugify a text string

    This function removes transliterates input string to ASCII, removes special characters
    and use join resulting elemets using specified separator.


    Parameters
    ----------
    input_string : str

    separator : string
        Default "-"
    lower : bool
        convert the result to lowercase (default True)
    make_set: bool
        return "set" object instead of string
    min_length: int
        minimal length of an element (word)
    slug_whitelist: str
        characters allowed in the output (default ascii letters, digits and the separator)
    split_chars:
        set of characters used for word splitting (there is a sane default)

    """
    separator = kwargs.get("separator", "-")
    lower = kwargs.get("lower", True)
    make_set = kwargs.get("make_set", False)
    min_lenght = int(kwargs.get("min_lenght", 1))
    slug_whitelist = kwargs.get("slug_whitelist", default_slug_whitelist)
    split_chars = kwargs.get("split_chars", slug_separator_whitelist)
    input_string = unaccent(input_string)
    if lower:
        input_string = input_string.lower()
    input_string = "".join([ch if ch not in split_chars else " " for ch in input_string])
    input_string = "".join([ch if ch in slug_whitelist + " " else "" for ch in input_string])
    elements = [elm.strip() for elm in input_string.split(" ") if len(elm.strip()) >= min_lenght]
    return set(elements) if make_set else separator.join(elements)

def string2color(string):
    """
    Generate more or less unique color for a given string
    """
    h = 0
    for char in string:
        h = ord(char) + ((h << 5) - h)
    return hex(h & 0x00FFFFFF)

def fract2float(fract):
    nd = fract.split("/")
    try:
        if len(nd) == 1 or nd[1] == "1":
            return float(nd[0])
        return float(nd[0]) / float(nd[1])
    except:
        return 1

def format_filesize(value):
    """
    Returns a human readable filesize for given byte count
    """
    if not value:
        return ""
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if value < 1024.0:
            return "%3.1f %s" % (value, x)
        value /= 1024.0
    return value
