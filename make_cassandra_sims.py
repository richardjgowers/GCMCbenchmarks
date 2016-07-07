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


def make_qsubmany(dirs, destination):
    """
    dirs - the simulation directories where qsubs can be found
    """
    outcontent = "#!/bin/bash\n\n"
    for d in dirs:
        outcontent += 'cd {}\n'.format(d)
        outcontent += 'qsub qsub.sh\n'
        outcontent += 'cd ../\n\n'

    qsubfn = os.path.join(destination, 'qsub_cas.sh')
    with open(qsubfn, 'w') as out:
        out.write(outcontent)
    os.chmod(qsubfn, 0744)  # rwxr--r-- permissions


def make_sims(pressure_values, case, destination):
    sourcedir = 'cassandra/cas_{}'.format(case)
    simdirs = []

    for p in pressure_values:
        suffix = 'cas_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
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
