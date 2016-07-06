#!/usr/bin/env python
"""Parse the results of a timing run

"""
from __future__ import print_function

from dateutil.parser import parse as parsetime
import glob
import os
import sys


def parse_timefile(d):
    """Return the time elapsed in a timing file in directory *d*

    Assumes a format:
     - comment line
     - date call 1
     - date call 2

    Returns
    -------
    number of seconds elapsed as integer
    """
    filename = glob.glob(os.path.join(d, 'timing*'))[0]
    t1, t2 = map(parsetime, open(filename, 'r').readlines()[1:])

    return (t2 - t1).seconds


def parse_cpuinfo(d):
    """Grab the results of a cpu query from directory *d*

    Returns
    -------
    string of the CPU info
    """
    # files will be result of cat /proc/cpuinfo > cpuinfo.$pressure
    filename = glob.glob(os.path.join(d, 'cpuinfo*'))[0]

    for line in open(filename, 'r'):
        if line.startswith('model name'):
            break
    # this line will look something like:
    # "model name : Intel 1234\n"
    return line.split(':')[1].strip()


def grab_times(prefix):
    """Grab all timings from directories starting with *prefix*

    Returns
    -------
    list of timings
    """
    timings = []

    for d in glob.glob('{}_*'.format(prefix)):
        try:
            time = parse_timefile(d)
            cpuinfo = parse_cpuinfo(d)
        except IndexError:
            continue
        else:
            timings.append((d, time, cpuinfo))
    return timings


if __name__ == '__main__':
    try:
        prefix = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage: {}  prefix".format(sys.argv[0]))
    else:
        print(grab_times(prefix))


        
