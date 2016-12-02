"""Common functions for results grabbing

"""
import functools
import glob
import os
import re

# regex match lazy anything, .o, then numerical chars
_O_PATTERN = re.compile('^.+?\.o[0-9]+$')
_O_MATCH = functools.partial(re.match, _O_PATTERN)


def _getnum(fname):
    """Return number from ofile name"""
    return int(fname.split('.o')[1])


def get_last_ofile(loc):
    """Return name of last o file"""
    # remove tilde files
    ofiles = filter(_O_MATCH,
                    glob.glob(os.path.join(loc, '*.o*')))

    return max(ofiles, key=_getnum)

