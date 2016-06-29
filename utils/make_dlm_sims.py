#!/usr/bin/env python
"""Make many DLMonte simulation directories

Requires a template folder to be given which contains
 - FIELD
 - CONFIG
 - CONTROL

Control file must have 'use gaspressure' and the pressure of CO2 set to '{pressure}'
"""
from __future__ import division

import sys
import os
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def kPa_to_kAtm(p):
    """Convert kPa to kAtm (dlmonte units)"""
    return p / 101325


def make_sims(pressure_values, suffix, destination):
    """Make many simulation directories

    pressure_values - list of pressues in kPa to make simulations for
    prefix - directory where template files can be found
    destination - directory to place new simulation files in
    """
    for p in pressure_values:
        newdir = os.path.join(destination, 'dlm_{}'.format(p))
        sourcedir = 'dlm_{}'.format(suffix)
        os.mkdir(newdir)
        # Files that don't change between runs
        for f in ['FIELD', 'CONFIG']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))
        # Files that need customising for this pressure
        template = open(os.path.join(sourcedir, 'CONTROL'), 'r').read()
        with open(os.path.join(newdir, 'CONTROL'), 'w') as out:
            out.write(template.format(pressure=kPa_to_kAtm(p)))


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise ValueError("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
