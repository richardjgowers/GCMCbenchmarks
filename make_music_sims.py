#!/usr/bin/env python
"""Create Music benchmark simulations

Usage:
  make_music_sims <case> <destination> [-n NSTEPS -s NSAMP -c NCOORD]

Options:
  -h --help   Show this screen
  --version   Show version
  -n          Total number of steps in simulations        [default: 11000000]
  -s          Number of steps between writing results     [default: 1000]
  -c          Number of steps between writing coordinates [default: 100000]
  -p          Pressures to create directories for

"""
from __future__ import division

from docopt import docopt
import os
import sys
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]
FUGACITY = {
    5: 4.996, 10: 9.985, 20: 19.94, 30: 29.86,
    40: 39.76, 50: 49.62, 60: 59.46, 70: 69.26
}
RUN_LENGTH = 11000000
SAVE_FREQ = 1000
COORDS_FREQ = 10000


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_mus.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0744)  # rwxr--r-- permissions


def make_sims(pressure_values, case, destination, **options):
    sourcedir = 'music/mus_{}'.format(case)
    simdirs = []  # all simulation directories

    for p in pressure_values:
        suffix = 'mus_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        # Make directory for this pressure point
        os.mkdir(newdir)
        # Copy files that don't get modified
        for f in ['atom_atom_all', 'fluid_properties.dat', 'pressure.dat',
                  'intra', 'mol_mol_all', 'post.ctr',
                  'setpath']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))
        # fugacity.dat gets pressure put inside of it
        template = open(os.path.join(sourcedir, 'fugacity.dat'), 'r').read()
        with open(os.path.join(newdir, 'fugacity.dat'), 'w') as out:
            out.write(template.format(
                fugacity=FUGACITY[p],
            ))
        # gcmc.ctr has runlength options
        template = open(os.path.join(sourcedir, 'gcmc.ctr'), 'r').read()
        with open(os.path.join(newdir, 'gcmc.ctr'), 'w') as out:
            out.write(template.format(
                run_length=options.get('run_length', RUN_LENGTH // 2),
                coords_freq=options.get('coords_freq', COORDS_FREQ),
                save_freq=options.get('save_freq', SAVE_FREQ),
            ))
        template = open(os.path.join(sourcedir, 'qsub.sh'), 'r').read()
        with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
            out.write(template.format(pressure=p))

    # These are common across all pressure directories
    for d in ('atoms', 'molecules', 'pmaps_krista'):
        shutil.copytree(os.path.join(sourcedir, '../', d),
                        os.path.join(destination, d))

    make_qsubmany(simdirs, destination)


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
