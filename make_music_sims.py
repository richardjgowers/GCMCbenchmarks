#!/usr/bin/env python
from __future__ import division

import os
import sys
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def make_sims(pressure_values, case, destination):
    sourcedir = 'music/mus_{}'.format(case)

    os.mkdir(os.path.join(destination, 'mus_{}'.format(case)))
    for f in ['atom_atom_all', 'fluid_properties.dat', 'fugacity.dat',
              'gcmc.ctr', 'intra', 'mol_mol_all', 'post.ctr', 'pressure.dat',
              'qsub.sh', 'setpath']:
        shutil.copy(os.path.join(sourcedir, f),
                    os.path.join(destination, 'mus_{}'.format(case), f))
    for d in ['atoms', 'molecules', 'pmaps_krista']:
        shutil.copytree(os.path.join(sourcedir, '../', d),
                        os.path.join(destination, d))


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        if not os.path.exists(os.path.join(os.getcwd(), destination)):
            os.mkdir(destination)
        elif not os.path.isdir(os.path.join(os.getcwd(), destination)):
            raise SystemExit
        make_sims(PRESSURES, prefix, destination)
