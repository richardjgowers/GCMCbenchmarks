#!/usr/bin/env python
"""Make Raspa benchmark simulations

"""
from __future__ import division

from docopt import docopt
import itertools
import os
import sys
import shutil

from gcmcbenchmarks.templates import raspa, makestr, PRESSURES
from gcmcbenchmarks.templates.raspa import steps_to_cycles


def kPa_to_Pa(pressure):
    return pressure * 1000.0


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_rsp.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0744)  # rwxr--r-- permissions


def make_sims(pressure_values, case, destination, options):
    sourcedir = getattr(raspa, case)
    simdirs = []

    try:
        nsteps = int(options['-n'])
    except ValueError:
        nsteps = map(int, options['-n'].split(','))
    else:
        nsteps = itertools.cycle((nsteps,))

    for p, n in zip(pressure_values, nsteps):
        suffix = 'rsp_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        for f in ['CO2.def', 'force_field.def', 'framework.def',
                  'IRMOF-1.cif', 'pseudo_atoms.def']:
            shutil.copy(sourcedir[f],
                        os.path.join(newdir, f))

            with open(sourcedir['simulation.input'], 'r') as inf:
                template = inf.read()
            with open(os.path.join(newdir, 'simulation.input'), 'w') as out:
                out.write(template.format(
                    pressure=kPa_to_Pa(p),
                    run_length=steps_to_cycles(n, case, p),
                    save_freq=steps_to_cycles(int(options['-s']), case, p),
                    coords_freq=steps_to_cycles(int(options['-c']), case, p),
                ))
            with open(sourcedir['qsub.sh'], 'r') as inf:
                qsub_template = inf.read()
            with open(os.path.join(newdir, 'qsub.sh'), 'w') as out:
                out.write(qsub_template.format(pressure=p))

    make_qsubmany(simdirs, destination)


if __name__ == '__main__':
    tot = __doc__ + makestr

    args = docopt(tot)

    if args['-p']:
        pressures = [int(p) for p in args['<pressures>']]
    else:
        pressures = PRESSURES

    destination = args['<dir>']

    if not os.path.exists(os.path.join(os.getcwd(), destination)):
        os.mkdir(destination)
    elif not os.path.isdir(os.path.join(os.getcwd(), destination)):
        raise SystemExit

    make_sims(pressures, args['<case>'], destination, args)

