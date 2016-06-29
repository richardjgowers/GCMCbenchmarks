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
import os

import make_towhee_sims
import make_dlm_sims


# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def make_runscripts(pressures, destination):
    """Make many runscripts

    One runscript for each pressure point, so that timing across a given pressure is consistent

    Arguments
    ---------
    pressures
      list of pressure values
    destination
      folder to create runscripts inside
    """
    for p in pressures:
        with open(os.path.join(destination, 'qsub_{}.sh'.format(p)), 'w') as out:
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

    with open(os.path.join(destination, 'qsuball.sh'), 'w') as out:
        out.write("#!/bin/bash\n")
        out.write("\n")
        for p in pressures:
            out.write("qsub qsub_{}.sh\n".format(p))



def make_all_sims(pressures, suffix, destination):
    """Make all simulation directories for all programs

    Arguments
    ---------
    pressures
      list of pressure values to create simulations for
    suffix
      the suffix inside each program's templates to use (case1/case2/case3)
    destination
      directory to place the new simulation inputs in
    """
    # make destination folder
    os.mkdir(destination)

    make_dlm_sims.make_sims(pressures, suffix, destination)
    make_towhee_sims.make_sims(pressures, suffix, destination)
    make_runscripts(pressures, destination)


if __name__ == '__main__':
    try:
        suffix, destination = sys.argv[1], sys.argv[2]
    except IndexError:
        raise SystemExit("Usage: {} templatesuffix destination".format(sys.argv[0]))
    else:
        make_all_sims(PRESSURES, suffix, destination)
