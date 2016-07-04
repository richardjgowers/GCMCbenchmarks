#!/usr/bin/env python
"""Make many Cassandra simulations

"""
import sys
import os
import shutil

# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]

# calculated in FugacityCalc notebook
# in kJ/mol
CHEMPOTS = {
    5:-31.7610427,
    10:-30.5636844,
    20:-29.3677046,
    30:-28.6692478,
    40:-28.1744894,
    50:-27.7913478,
    60:-27.4788076,
    70:-27.2149899,
}

def make_sims(pressure_values, suffix, destination):
    sourcedir = 'cassandra/cas_{}'.format(suffix)
    for p in pressure_values:
        newdir = os.path.join(destination, 'cas_{}'.format(p))
        os.mkdir(newdir)

        # Copy over individual files
        for f in ['CO2.ff', 'CO2.mcf', 'CO2.pdb',
                  'IRMOF.ff', 'IRMOF.mcf', 'IRMOF.pdb', 'IRMOF.xyz']:
            shutil.copy(os.path.join(sourcedir, f),
                        os.path.join(newdir, f))
        # Copy over directories
        for d in ['species1', 'species2']:
            shutil.copytree(os.path.join(sourcedir, d),
                            os.path.join(newdir, d))
        # Copy and edit input file
        template = open(os.path.join(sourcedir, 'CO2_IRMOF.inp'), 'r').read()
        with open(os.path.join(newdir, 'CO2_IRMOF.inp'), 'w') as out:
            out.write(template.format(chempot=CHEMPOTS[p]))


if __name__ == '__main__':
    try:
        prefix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatedir destination".format(sys.argv[0]))
    else:
        make_sims(PRESSURES, prefix, destination)
