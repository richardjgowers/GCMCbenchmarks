import glob
import re
import os
import pandas as pd


from . import (
    cassandra_parser as cas,
    dlmonte_parser as dlm,
    music_parser as mus,
    raspa_parser as rsp,
    towhee_parser as twh,
)


def format_parser(dirname):
    if 'dlm' in dirname:
        return dlm.grab_timeseries
    elif 'twh' in dirname:
        return twh.grab_timeseries
    elif 'rsp' in dirname:
        return rsp.grab_timeseries
    elif 'mus' in dirname:
        return mus.grab_timeseries
    else:  # cas is in most because I called directories '_case1_'
        return cas.grab_timeseries


def find_simdirs(d):
    simdirs = {}
    for subdir in glob.glob(os.path.join(d, '*')):
        mat = re.match('.+?\/\w{3}_(\d+)', subdir)
        if not mat is None:
            simdirs[int(mat.groups()[0])] = subdir
    return simdirs


def find_equil(ser):
    # find where it reaches equilibrium and shift back data
    # return the eq step number
    ser = pd.Series(ser)
    # assume at least half the data is equilibrated
    # (visually inspect for this)
    n = len(ser)
    half = n // 4
    mean = ser.values[3*half:].mean()
    std = ser.values[3*half:].std()
    
    # For series of length less than 100, use a "window" of 1
    nwindow = max(n // 100, 1)
    
    eq = ser[ser.rolling(nwindow).mean() > mean - 1.5 * std].index[0]
    
    return eq


def grab_all_results(d):
    """Return all results from directory d"""
    subdir_parser = format_parser(d)  # appropriate timeseries getter for this directory

    subdirs = find_simdirs(d)

    final = []
    pressures = []
    for p, subdir in subdirs.items():
        # raw timeseries results
        results = subdir_parser(subdir)
        
        eq = find_equil(results)

        pressures.append(p)

        final.append((results[eq:].mean(), results[eq:].std()))

    return pd.DataFrame(final, pressures, columns=['mean', 'std']).sort_index()

def parse(d, ignore_incomplete=False):
    """Return timeseries from directory *d*"""
    return format_parser(d)(d, ignore_incomplete)
