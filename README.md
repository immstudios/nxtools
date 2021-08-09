nxtools
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


### CasparCG

CasparCG client object

### CasparResponse

Caspar query response object

### FileObject

An object representing a file on the filesystem.

The class provides a number of utility methods and properties
for easy access to file metadata.
### critical_error

Log an error message and exit program.

### datestr2ts

Convert a `YYYY-MM-DD` string to an unix timestamp.

By default, start of the day (midnight) is returned.

```
Args:
    datestr (str):
        `YYYY-MM-DD` string

    hh (int):
        Hour (default: 0)

    mm (int):
        Minute (default: 0)

    ss (int):
        Second (default: 0)

Returns:
    int:
        Parsed unix timestamp
```

### f2tc

Convert frames to an SMPTE timecode


```
Args:
    frames (int):
        Frame count

    base (float):
        Frame rate (default: 25)

Returns:
    str:
        SMPTE timecode (`HH:MM:SS:FF`)
```

### ffmpeg

FFMpeg wrapper with progress and error handling


```
Args:
    *args (list[any]): 
        List of ffmpeg command line arguments.
        Each argument is converted to a string.

    progress_handler (function):
        Function to be called with the current position (seconds) as argument.

    stdin (file):
        File object to be used as stdin.
        Default is subprocess.PIPE

    stdout (file):
        File object to be used as stdout.
        Default is None

    stderr (file):
        File object to be used as stderr.
        Default is subprocess.PIPE (used to compute progress).

    debug (bool):
        Enable debug mode (write ffmpeg output to stderr).

Returns:
    boolean: indicate if the process was successful
```

### ffprobe

Extract metadata from a media file using ffprobe
and returns a dictionary object with the result

```
Args:
    input_file (str): 
        Path to the media file

    verbose (bool): 
        Log the ffprobe command. Default is False

Returns:
    dict: metadata
```

### file_to_title

Attempt to un-slugify a file name

### filter_arc

Aspect ratio convertor. you must specify output size and source aspect ratio (as float)

### filter_deinterlace

Yadif deinterlace

### find_binary

Attempt to find a given executable and return its path


```
Args:
    file_name (str): The name of the executable to find

Returns:
    str: The path to the executable
```

### format_filesize

Return a human readable filesize for a given byte count

### format_time

Format an Unix timestamp as a local or GMT time


```
Args:
    timestamp (int):
        input unix timestamp

    time_format (str):
        strftime specification
        (default: "%Y-%m-%d %H:%M:%S" - the correct one)

    never_placeholder (str):
        text used when timestamp is not specified (default: "never")

    gmt (bool):
        Use GMT time instead of local time (default: False)

Returns:
    str:
        Formatted time
```

### get_base_name

Strip a directory and extension from a given path.

`/etc/foo/bar.baz` becomes `bar`

```
Args:
    file_name (str): path-like object, string or FileObject

Returns:
    str
```

### get_files

Crawl a given directory

For each file found in `base_path` yield a FileObject object.

```
Args:
    base_path (str):
        Path to the directory to be crawled

    recursive (bool):
        Crawl recursively (default: False)

    hidden (bool):
        Yield hidden (dot)files too (default: False)

    exts (list):
        If specified, yields only files matching given extensions

    case_sensitive_exts (bool):
        Do not ignore cases when `exts` list is used (default: False)
```

### get_guid

Return a GUID

Returns:
str: GUID
### get_path_pairs

For each file found in `input_dir` and yield a tuple of (input_path, output_path)

This function is useful for batch conversion, when you need to process files
from `input_dir` and output the result to `output_dir`.

Most arguments are the same as for `get_files`. You can also specify a target extension,
and use a slugifier for the output path.

```
Args:
    target_ext (str):
    target_slugify (bool): (default: False)
```

### get_temp

Return a path to a temporary file


```
Args:
    extension (str)
    root (str)
```

### indent

Indent a multi-line text

### join_filters

Joins multiple filters

### log_traceback

Log the current exception traceback

### s2tc

Convert seconds to an SMPTE timecode


```
Args:
    secs (float):
        Number of seconds

    base (float):
        Frame rate (default: 25)

Returns:
    str:
        SMPTE timecode (`HH:MM:SS:FF`)
```

### s2time

Convert seconds to time


```
Args:
    secs (float):

    show_secs (bool):
        Show seconds (default: True)

    show_fracs (bool):
        Show centiseconds (default: True)

Returns:
    str:
        `HH:MM` / `HH:MM:SS` / `HH:MM:SS.CS` string
```

### s2words

Create a textual (english) representation of given number of seconds.

This function is useful for showing estimated time of a process.

```
Args:
    secs (int):
        Number of seconds

Returns:
    str:
        Textual information
```

### slugify

Slugify a text string

This function removes transliterates input string to ASCII, removes special characters
and use join resulting elemets using specified separator.

```
Args:
    input_string (str):
        Input string to slugify

    separator (str): 
        A string used to separate returned elements (default: "-")

    lower (bool): 
        Convert to lower-case (default: True)

    make_set (bool):
        Return "set" object instead of string

    min_length (int): 
        Minimal length of an element (word)

    slug_whitelist (str): 
        Characters allowed in the output
        (default: ascii letters, digits and the separator)

    split_chars (str): 
        Set of characters used for word splitting (there is a sane default)
```

### string2color

Generate more or less unique color for a given string

### tc2s

Convert an SMPTE timecode (HH:MM:SS:FF) to number of seconds


```
Args:
    tc (str):
        Source timecode

    base (float):
        Frame rate (default: 25)

Returns:
    float:
        Resulting value in seconds
```

### unaccent

Remove accents and/or transliterate non-ascii characters

### xml

Parse an XML string using ElementTree


```
Args:
    data (str): The XML document to parse

Returns:
    ElementTree.Element: The root element of the parsed XML string
```
