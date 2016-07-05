#!/usr/bin/env python
from __future__ import division

import os
import sys
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]

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

def Steps_to_Cycles(Steps, case, pressure):
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
    trans = NMOL[case]

    return Steps / trans[pressure]


def kPa_to_Pa(pressure):
    return pressure * 1000.0


def make_sims(pressure_values, suffix, destination):
    sourcedir = 'raspa/rsp_{}'.format(suffix)

    for p in pressure_values:
        newdir = os.path.join(destination, 'rsp_{}'.format(p))
        os.mkdir(newdir)

        for f in ['CO2.def', 'force_field.def', 'framework.def',
                  'IRMOF-1.cif', 'pseudo_atoms.def']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))

            template = open(os.path.join(sourcedir, 'simulation.input'), 'r').read()
            with open(os.path.join(newdir, 'simulation.input'), 'w') as out:
                out.write(template.format(pressure=kPa_to_Pa(p)))


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
