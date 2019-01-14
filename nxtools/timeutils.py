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

import time
import datetime

__all__ = ["datestr2ts", "tc2s", "s2time", "f2tc", "s2tc", "s2words", "format_time"]


def datestr2ts(datestr, hh=0, mm=0, ss=0):
    """Converts YYYY-MM-DD string to unix timestamp. Additionally hh, mm and ss params can be used"""
    yy, mo, dd = [int(i) for i in datestr.split("-")]
    ttuple = [yy, mo, dd, hh, mm]
    dt = datetime.datetime(*ttuple)
    tstamp = time.mktime(dt.timetuple())
    return tstamp

def tc2s(tc, base=25):
    tc = tc.replace(";", ":")
    hh, mm, ss, ff = [int(e) for e in tc.split(":")]
    res = hh * 3600
    res += mm * 60
    res += ss
    res += ff / float(base)
    return res

def s2time(secs, show_secs=True, show_fracs=True):
    """Converts seconds to time"""
    try:
        secs = float(secs)
    except:
        return "--:--:--.--"
    wholesecs = int(secs)
    centisecs = int((secs - wholesecs) * 100)
    hh = int(wholesecs / 3600)
    hd = int(hh % 24)
    mm = int((wholesecs / 60) - (hh*60))
    ss = int(wholesecs - (hh*3600) - (mm*60))
    r = "{:02d}:{:02d}".format(hd, mm)
    if show_secs:
        r += ":{:02d}".format(ss)
    if show_fracs:
        r += ".{:02d}".format(centisecs)
    return r


def f2tc(f,base=25):
    """Converts frames to timecode"""
    try:
        f = int(f)
    except:
        return "--:--:--:--"
    hh = int((f / base) / 3600)
    mm = int(((f / base) / 60) - (hh*60))
    ss = int((f/base) - (hh*3600) - (mm*60))
    ff = int(f - (hh*3600*base) - (mm*60*base) - (ss*base))
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hh, mm, ss, ff)


def s2tc(s,base=25):
    """Converts seconds to timecode"""
    try:
        f = int(s*base)
    except:
        return "--:--:--:--"
    hh  = int((f / base) / 3600)
    hhd = int((hh % 24))
    mm  = int(((f / base) / 60) - (hh*60))
    ss  = int((f/base) - (hh*3600) - (mm*60))
    ff  = int(f - (hh*3600*base) - (mm*60*base) - (ss*base))
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hhd, mm, ss, ff)


def s2words(s):
    s = int(s)
    if s < 60:
        return "{} seconds".format(s)
    elif s < 120:
        return "1 minute {} seconds".format(int(s-60))
    elif s < 7200:
        return "{} minutes".format(int(s/60))
    else:
        return "{} hours".format(int(s/3600))


def format_time(timestamp, time_format="%Y-%m-%d %H:%M:%S", never_placeholder="never"):
    """strftime/localtime shortcut"""
    if not timestamp:
        return never_placeholder
    return time.strftime(time_format, time.localtime(timestamp))
