"""Grab all results from dlm runs

for each dlm_* directory:
   check OUTPUT exists?
   check OUTPUT exited correctly?
   read the results
"""
import numpy as np
import os


def check_exit(loc):
    """Check that simulation in *loc* exited correctly."""
    output = os.path.join(loc, 'OUTPUT.000')

    # check results have been generated
    if not os.path.exists(output):
        raise ValueError("Output not present in dir: {}".format(loc))
    # check results ended correctly
    with open(output, 'r') as f:
        f.seek(-100, 2)  # seek to 100 before EOF (2)
        if not f.read().strip().endswith('normal exit'):
            raise ValueError("Output didn't exit correct in dir: {}".format(loc))

    return True


def grab_timeseries(loc):
    check_exit(loc)

    output = os.path.join(loc, 'OUTPUT.000')

    # grab lines beginning with ' CO2'
    results = []
    for line in open(output, 'r'):
        if line.startswith(' CO2'):
            try:
                results.append(float(line.split()[1]))
            except (ValueError, IndexError):
                pass
    # last result is an average, discard it
    return np.array(results[:-1]) / 8.0  # to mol/uc
