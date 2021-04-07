nxtools
=======

nxtools is a set of various tools and helpers used by [Nebula](https://github.com/nebulabroadcast/nebula) and other software.

Installation
------------

``pip install nxtools``

Examples
-------

 - [Podcasts downloader](https://pastebin.com/5Fya2kep>)

Reference
---------


### critical_error

Log an error message and exit program.

### datestr2ts

Converts YYYY-MM-DD string to unix timestamp.

By default, start of the day (midnight) is returned.

```
Args:
    datestr (str): `YYYY-MM-DD` string
    hh (int): Hour
    mm (int): Minute
    ss (int): Second

Returns:
    int: Parsed unix timestamp
```

### f2tc

Converts frames to a SMPTE timecode


```
Args:
    f (int): Frame count
    base (float) : Frame rate (default: 25)

Returns:
    str: SMPTE timecode (HH:MM:SS:FF)
```

### find_binary

Attempt to find a given executable and return its path

### format_filesize

Returns a human readable filesize for a given byte count

### format_time

Format unix timestamp to the local or GMT time


```
Args:
    timestamp (int): input unix timestamp
    time_format (str): strftime specification (default: "%Y-%m-%d %H:%M:%S" - the correct one)
    never_placeholder (str): text used when timestamp is not specified (default: "never")
    gmt (bool): Use GMT time instead of local time (default: False)

Returns:
    str: Formatted time
```

### get_base_name

Strips a directory and and extension from a given path.

`/etc/foo/bar.baz` becomes `bar`

```
Args:
    fname (str): path-like object, string or FileObject

Returns:
    str
```

### get_files

Crawls a given directory (base_path) and yields a FileObject object for each file found.

Since scandir is used for crawling, file attributes (ctime, mtime, size...) are instantly available.

```
Args:
    base_path (str): Path to the directory to be crawled
    recursive (bool): Crawl recursively (default: False)
    hidden (bool): Yield hidden (dot)files too (default: False)
    exts (list): If specified, yields only files matching given extensions
    case_sensitive_exts (bool): Do not ignore cases when `exts` list is used (default: False)
```

### get_guid

Returns a GUID :)

### get_temp

Returns a path to a temporary file


```
Args:
    extension (str)
    root (str)
```

### indent

Indent a multi-line text

### log_traceback

Log the current exception traceback

### s2tc

Converts seconds to timecode


```
Args:
    s (float): Number of seconds
    base (float) : Frame rate (default: 25)

Returns:
    str: SMPTE timecode (HH:MM:SS:FF)
```

### s2time

Converts seconds to time


```
Args:
    secs (float):
    show_secs (bool): Show seconds (default: True)
    show_fracs (bool): Show centiseconds (default: True)

Returns:
    str: HH:MM / HH:MM:SS / HH:MM:SS.CS string
```

### s2words

Creates a textual (english) representation of given number of seconds.

This function is useful for showing estimated time of a process.

```
Args:
    s (int) : Number of seconds

Returns:
    str : Textual information
```

### slugify

Slugify a text string

This function removes transliterates input string to ASCII, removes special characters
and use join resulting elemets using specified separator.

"Žluťoučký Путин is 下衆野郎" becomes "zlutoucky-putin-is-xia-zhong-ye-lang"

```
Args:
    input_string (str):
    separator (str): string (default: "-")
    lower (bool): Convert to lower-case (default: True)
    make_set (bool): return "set" object instead of string
    min_lenght (int): minimal length of an element (word)
    slug_whitelist (str): characters allowed in the output
            (default ascii letters, digits and the separator)
    split_chars (str): set of characters used for word
            splitting (there is a sane default)
```

### string2color

Generate more or less unique color for a given string

### tc2s

Converts SMPTE timecode (HH:MM:SS:FF) to number of seconds


```
Args:
    tc (str): Source timecode
    base (float): Frame rate (default: 25)

Returns:
    float: Resulting value in seconds
```

### unaccent

Remove accents and/or transliterate non-ascii characters

### xml

Parse an XML using ElementTree
