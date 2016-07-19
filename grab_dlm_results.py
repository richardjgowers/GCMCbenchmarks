"""Grab all results from dlm runs

for each dlm_* directory:
   check OUTPUT exists?
   check OUTPUT exited correctly?
   read the results
"""
import glob
import numpy as np
import os


def parse_dir(loc):
    """Look inside *loc* and perform checks

    returns average mol/uc for this dir
    """
    output = os.path.join(loc, 'OUTPUT.000')

    # check results have been generated
    if not os.path.exists(output):
        raise ValueError("Output not present in dir: {}".format(loc))
    # check results ended correctly
    with open(output, 'r') as f:
        f.seek(-100, 2)  # seek to 100 before EOF (2)
        if not f.read().strip().endswith('normal exit'):
            raise ValueError("Output didn't exit correct in dir: {}".format(loc))
    # grab lines beginning with ' CO2'
    results = []
    for line in open(output, 'r'):
        if line.startswith(' CO2'):
            try:
                results.append(float(line.split()[-1]))
            except ValueError:
                pass
    # check length of results?
    return np.mean(results) / 8.0


def parse_dlm_results(loc=None):
    """Look inside *loc* for dlm directories and parse all

    returns {dirname: results}
    """
    if loc is None:
        loc = '.'
    dlm_dirs = os.path.join(loc, glob.glob("dlm_*"))

    return {d: parse_dir(d) for d in dlm_dirs}
