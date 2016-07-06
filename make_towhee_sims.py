#!/usr/bin/env python
"""Make a set of Towhee simulations

"""
from __future__ import division

import sys
import os
import shutil

# pressures in kPa to run
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]

# chemical potentials calculated in PREoS notebook
CHEMPOTS = {5:-3819.9767,
            10:-3675.9676,
            20:-3532.1242,
            30:-3448.1191,
            40:-3388.6133,
            50:-3342.5320,
            60:-3304.9420,
            70:-3273.2120,
}


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_twh.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0744)  # rwxr--r-- permissions


def make_sims(pressure_values, case, destination):
    sourcedir = 'towhee/twh_{}'.format(case)
    simdirs = []

    for p in PRESSURES:
        suffix = 'twh_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        for f in ['towhee_coords', 'towhee_ff_CUSTOM']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))

        template = open(os.path.join(sourcedir, 'towhee_input'), 'r').read()
        with open(os.path.join(newdir, 'towhee_input'), 'w') as out:
            out.write(template.format(chempot=CHEMPOTS[p]))
        qsub_template = open(os.path.join(sourcedir, 'qsub.sh'), 'r').read()
        with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
            out.write(qsub_template.format(pressure=p))

    make_qsubmany(simdirs, destination)


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
