"""Make all simulations

creates many directories with input files

prefix
cas - Cassandra
dlm - DL Monte
mus - Music
rsp - Raspa
twh - Towhee


"""
import textwrap
import sys

import make_towhee_sims
import make_dlm_sims


# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def make_runscripts(pressures):
    """Make many runscripts

    One runscript for each pressure point, so that timing across a given pressure is consistent
    """
    for p in pressures:
        with open('qsub_{}.sh'.format(p), 'w') as out:
            out.write(textwrap.dedent(
"""\
#!/bin/bash

#$ -N tmg_{pressure}
#$ -cwd
#$ -l h_rt=04:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cd cas_{pressure}
date
# cassandra exe
date
cd ../

cd dlm_{pressure}
date
#./DLMONTE-SRL.X
echo "run dlmonte"
date
cd ../

cd mus_{pressure}
date
# music exe
date
cd ../

cd rsp_{pressure}
date
# rsp exe
date
cd ../

cd twh_{pressure}
date
#./towhee
echo "run towhee"
date
cd ../
""".format(pressure=p)))


def make_all_sims(pressures, suffix):
    """Make all simulation directories for all programs

    """
    make_dlm_sims.make_sims(pressures, suffix)
    make_towhee_sims.make_sims(pressures, suffix)
    make_runscripts(pressures)


if __name__ == '__main__':
    try:
        suffix = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage: {} templatesuffix".format(sys.argv[0]))
    else:
        make_all_sims(PRESSURES, suffix)
