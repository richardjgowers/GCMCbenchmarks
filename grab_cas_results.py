"""Grab all results from cas runs


"""
import glob
import numpy as np
import os


def parse_dir(loc):
    """returns average mol/uc in this dir"""
    output = os.path.join(loc, 'CO2_IRMOF.box1.prp1')

    # check results exist
    if not os.path.exists(output):
        raise ValueError("Output not found in dir: {}".format(loc))
    # check run ended correctly
    # TODO

    # finally grab results
    results = []
    for line in open(output, 'r'):
        if line.startswith('#'):
            continue
        results.append(float(line.split()[3]))

    return np.mean(results) / 8.0


def parse_cas_results(loc):
    """Grab results from all cas_* directories

    Returns {dirname: avg mol/uc} for each dir
    """
    return {d: parse_dir(d) for d in glob.glob('cas_*')}
