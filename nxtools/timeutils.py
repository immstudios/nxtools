__all__ = [
    "datestr2ts",
    "tc2s",
    "s2time",
    "f2tc",
    "s2tc",
    "s2words",
    "format_time"
]

import time
import datetime


def datestr2ts(datestr:str, hh:int=0, mm:int=0, ss:int=0) -> int:
    """Converts a `YYYY-MM-DD` string to an unix timestamp.

    By default, start of the day (midnight) is returned.

    Args:
        datestr (str): `YYYY-MM-DD` string
        hh (int): Hour
        mm (int): Minute
        ss (int): Second

    Returns:
        int: Parsed unix timestamp
    """
    yy, mo, dd = [int(i) for i in datestr.split("-")]
    ttuple = [yy, mo, dd, hh, mm]
    dt = datetime.datetime(*ttuple)
    tstamp = int(time.mktime(dt.timetuple()))
    return tstamp


def tc2s(tc:str, base:float=25) -> float:
    """Converts an SMPTE timecode (HH:MM:SS:FF) to number of seconds

    Args:
        tc (str): Source timecode
        base (float): Frame rate (default: 25)

    Returns:
        float: Resulting value in seconds
    """
    tc = tc.replace(";", ":")
    hh, mm, ss, ff = [int(e) for e in tc.split(":")]
    res = hh * 3600
    res += mm * 60
    res += ss
    res += ff / float(base)
    return res


def s2time(secs:float, show_secs:bool=True, show_fracs:bool=True):
    """Converts seconds to time

    Args:
        secs (float):
        show_secs (bool): Show seconds (default: True)
        show_fracs (bool): Show centiseconds (default: True)

    Returns:
        str: HH:MM / HH:MM:SS / HH:MM:SS.CS string
    """
    try:
        secs = max(0, float(secs))
    except:
        placeholder = "--:--"
        if show_secs:
            placeholder += ":--"
            if show_fracs:
                placeholder += ".--"
        return placeholder
    wholesecs = int(secs)
    centisecs = int((secs - wholesecs) * 100)
    hh = int(wholesecs / 3600)
    hd = int(hh % 24)
    mm = int((wholesecs / 60) - (hh*60))
    ss = int(wholesecs - (hh*3600) - (mm*60))
    r = f"{hd:02d}:{mm:02d}"
    if show_secs:
        r += f":{ss:02d}"
        if show_fracs:
            r += f".{centisecs:02d}"
    return r

def f2tc(f, base=25):
    """Converts frames to a SMPTE timecode

    Args:
        f (int): Frame count
        base (float) : Frame rate (default: 25)

    Returns:
        str: SMPTE timecode (HH:MM:SS:FF)
    """
    try:
        f = max(0, int(f))
    except:
        return "--:--:--:--"
    hh = int((f / base) / 3600)
    mm = int(((f / base) / 60) - (hh*60))
    ss = int((f/base) - (hh*3600) - (mm*60))
    ff = int(f - (hh*3600*base) - (mm*60*base) - (ss*base))
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def s2tc(s, base=25):
    """Converts seconds to timecode

    Args:
        s (float): Number of seconds
        base (float) : Frame rate (default: 25)

    Returns:
        str: SMPTE timecode (HH:MM:SS:FF)
    """
    try:
        f = max(0, int(s*base))
    except:
        return "--:--:--:--"
    hh = int((f / base) / 3600)
    hd = int((hh % 24))
    mm = int(((f / base) / 60) - (hh*60))
    ss = int((f/base) - (hh*3600) - (mm*60))
    ff = int(f - (hh*3600*base) - (mm*60*base) - (ss*base))
    return f"{hd:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def s2words(s):
    """Creates a textual (english) representation of given number of seconds.

    This function is useful for showing estimated time of a process.

    Args:
        s (int) : Number of seconds

    Returns:
        str : Textual information
    """
    s = int(s)
    if s < 60:
        return f"{s} seconds".format(s)
    elif s < 120:
        return f"1 minute {int(s-60)} seconds"
    elif s < 7200:
        return f"{int(s/60)} minutes"
    else:
        return f"{int(s/3600)} hours"


def format_time(timestamp=None, time_format="%Y-%m-%d %H:%M:%S", never_placeholder="never", gmt=False):
    """Formats unix timestamp to the local or GMT time

    Args:
        timestamp (int): input unix timestamp
        time_format (str): strftime specification (default: "%Y-%m-%d %H:%M:%S" - the correct one)
        never_placeholder (str): text used when timestamp is not specified (default: "never")
        gmt (bool): Use GMT time instead of local time (default: False)

    Returns:
        str: Formatted time
    """
    if not timestamp:
        return never_placeholder
    return time.strftime(time_format, time.gmtime(timestamp) if gmt else time.localtime(timestamp))
