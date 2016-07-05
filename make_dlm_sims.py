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


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_dlm.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0744)  # rwxr--r-- permissions


def make_sims(pressure_values, case, destination):
    """Make many simulation directories

    pressure_values - list of pressues in kPa to make simulations for
    case - directory where template files can be found
    destination - directory to place new simulation files in
    """
    sourcedir = 'dlmonte/dlm_{}'.format(case)
    simdirs = []

    for p in pressure_values:
        suffix = 'dlm_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        # Files that don't change between runs
        for f in ['FIELD', 'CONFIG']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))
        # Files that need customising for this pressure
        template = open(os.path.join(sourcedir, 'CONTROL'), 'r').read()
        with open(os.path.join(newdir, 'CONTROL'), 'w') as out:
            out.write(template.format(pressure=kPa_to_kAtm(p)))
        qsub_template = open(os.path.join(sourcedir, 'qsub.sh'), 'r').read()
        with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
            out.write(qsub_template.format(pressure=p))
    # Make convenience script for starting jobs
    make_qsubmany(simdirs, destination)


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
