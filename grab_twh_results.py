import glob
import numpy as np
import os


def _get_last_ofile(loc):
    """Return name of last o file"""
    ofiles = glob.glob(os.path.join(loc, 'twh_*.o*'))
    last = max(int(n.split('o')[1]) for n in ofiles)

    return [f for f in ofiles if str(last) in f][0]

def parse_dir(loc):
    # grab last .o file
    ofile = _get_last_ofile(loc)

    rawlines = []
    for line in open(ofile, 'r'):
        if line.startswith(' Molecule Number                2'):
            rawlines.append(line.strip())

    return float(rawlines[0].split()[-1]) / 8.0


def parse_twh_results(loc=None):
    """Grab all Towhee results from location *loc*"""
    if loc is None:
        loc = '.'
    return {d: parse_dir(d)
            for d in glob.glob(os.path.join(loc, 'twh_*'))}
