#!/usr/bin/env python
"""Make Raspa benchmark simulations

"""
from __future__ import division

from docopt import docopt
import os
import sys
import shutil

from gcmcbenchmarks.templates import raspa, makestr, PRESSURES

# Average number of molecules at a given pressure (ie the result)
# Used to translate between steps and cycles for benchmarking
#
# This changes depending on which case is done, so dict for each
_NMOL_case1 = {  # LJ only
    5 : 4.09 * 8,  # result in mol/uc then *8 because 2x2x2 sim box
    10 : 8.70 * 8,
    20 : 18.57 * 8,
    30 : 30.84 * 8,
    40 : 48.06 * 8,
    50 : 79.01 * 8,
    60 : 115.95 * 8,
    70 : 133.53 * 8,
}
_NMOL_case2 = {  # LJ and FF electrostatics
    5 : 4.26 * 8,
    10 : 9.39 * 8,
    20 : 25.44 * 8,
    30 : 179.30 * 8,
    40 : 185.95 * 8,
    50 : 189.64 * 8,
    60 : 193.60 * 8,
    70 : 194.98 * 8,
}
_NMOL_case3 = {  # LJ and all electrostatics
    5 : 7.66 * 8,
    10 : 16.39 * 8,
    20 : 167.60 * 8,
    30 : 183.32 * 8,
    40 : 190.16 * 8,
    50 : 193.94 * 8,
    60 : 196.35 * 8,
    70 : 198.15 * 8,
}
NMOL = {
    'case1':_NMOL_case1,
    'case2':_NMOL_case2,
    'case3':_NMOL_case3,
}

def steps_to_cycles(steps, case, pressure):
    """Translate a number of steps to cycles

    Parameters
    ----------
    Steps
      Number of Monte Carlo moves desired
    case
      System conditions [case1/case2/case3]
    pressure
      Pressure in kPa

    Returns
    -------
    number of cycles
    """
    # select the pressure->nmol dict to use
    trans = NMOL[case[:5]]

    # need integer number of cycles, minimum of 1
    return max(int(steps / trans[pressure]), 1)


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

    for p in pressure_values:
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
                    run_length=steps_to_cycles(int(options['-n']), case, p),
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

