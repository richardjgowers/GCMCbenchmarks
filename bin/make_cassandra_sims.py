#!/usr/bin/env python
"""Make many Cassandra simulations

"""
from docopt import docopt
from itertools import cycle
import sys
import os
import shutil

from gcmcbenchmarks.templates import cassandra, makestr, PRESSURES

# pressure: chempot in kJ/mol
CHEMPOTS = cassandra.CHEMPOTS


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


def make_sims(pressure_values, case, destination, options):
    sourcedir = getattr(cassandra, case)
    simdirs = []

    try:
        nsteps = int(options['-n'])
    except ValueError:
        nsteps = map(int, options['-n'].split(','))
    else:
        nsteps = itertools.cycle((nsteps,))

    for p, n in zip(pressure_values, nsteps):
        suffix = 'cas_{}'.format(p)
        simdirs.append(suffix)
        newdir = os.path.join(destination, suffix)
        os.mkdir(newdir)

        # Copy over individual files
        for f in ['CO2.ff', 'CO2.mcf', 'CO2.pdb',
                  'IRMOF.ff', 'IRMOF.mcf', 'IRMOF.pdb', 'IRMOF.xyz']:
            shutil.copy(sourcedir[f],
                        os.path.join(newdir, f))
        # Copy in directories
        # cas_20/species2/frag1/
        # cas_20/species2/fragments/
        sp2 = os.path.join(newdir, 'species2')
        os.mkdir(sp2)
        for d in ['frag1', 'fragments']:
            subdir = os.path.join(sp2, d)
            os.mkdir(subdir)
            for f in sourcedir[d]:
                shutil.copy(sourcedir[d][f],
                            os.path.join(subdir, f))

        # Copy and edit input file
        template = open(sourcedir['CO2_IRMOF.inp'], 'r').read()
        with open(os.path.join(newdir, 'CO2_IRMOF.inp'), 'w') as out:
            out.write(template.format(
                chempot=CHEMPOTS[p],
                run_length=n,
                save_freq=int(options['-s']),
                coords_freq=int(options['-c']),
            ))
        qsub_template = open(sourcedir['qsub.sh'], 'r').read()
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
