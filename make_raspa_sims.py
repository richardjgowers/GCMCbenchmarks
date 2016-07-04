#!/usr/bin/env python

import os
import sys
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def kPa_to_Pa(pressure):
    return pressure * 1000.0


def make_sims(pressure_values, suffix, destination):
    sourcedir = 'raspa/ras_{}'.format(suffix)

    for p in pressure_values:
        newdir = os.path.join(detination, 'ras_{}'.format(p))
        os.mkdir(newdir)

        for f in ['CO2.def', 'force_field.def', 'framework.def',
                  'IRMOF-1.cif', 'pseudo_atoms.def']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))

            template = open(os.path.join(sourcedir, 'simulation.input')).read()
            with open(os.path.join(newdir, 'simulation.input')) as out:
                out.write(template.format(pressure=kPa_to_Pa(p)))


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
