"""Make multiple simulations of one for towhee

eg:

[2, 4] gives:

twh_par_2 -> towhee  # binary
          -> towhee_parallel  # parallel file
          -> twh_2_1  # working directory for each parallel run
          -> twh_2_2
twh_par_4 -> towhee
          -> towhee_parallel
          -> twh_4_1
          -> twh_4_2
          -> twh_4_3
          -> twh_4_4

"""
import sys
import textwrap
import os
import shutil


from make_towhee_sims import make_sims

PRESSURES = [70]

_QSUB_HEADER = textwrap.dedent(
"""\
#!/bin/sh
#$ -N twh_parallel
#$ -pe mpi 16
#$ -cwd
#$ -l h_rt=48:00:00

. /etc/profile.d/modules.sh
module load intel/2016
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.out

""")


def make_parallel_sims(cores, destination):
    """
    cores = [1, 3, 4, 8, 16, 32]
    """
    os.mkdir(destination)

    # Create a parallel place for each number of cores
    for c in cores:
        dirname = 'twh_par_{}'.format(c)
        newdir = os.path.join(destination, dirname)
        os.mkdir(newdir)

        # Create *c* copies of the simulation in this directory
        for p in xrange(c):
            make_sims(PRESSURES, 'case1', newdir)
            # Rename so that another version can be created
            os.rename(os.path.join(newdir, 'twh_70'),
                      os.path.join(newdir, 'twh_{}_{}'.format(c, p)))

        # Create the towhee_parallel file
        with open(os.path.join(newdir, 'towhee_parallel'), 'w') as out:
            out.write("#number of jobs\n")
            out.write("{}\n".format(c))
            out.write("#stdout file\n")
            out.write("parallel.out\n")
            out.write("#working directories\n")
            for p in xrange(c):
                out.write("twh_{}_{}\n".format(c, p))

    # make a qsub file
    with open(os.path.join(destination, 'qsub.sh'), 'w') as out:
        # Standard job submission
        out.write(_QSUB_HEADER)
        # for each number of cores, run the simulation
        for c in cores:
            out.write("cd twh_par_{}\n".format(c))
            out.write("echo 'Doing run for {} cores' >> timing.$JOB_ID\n".format(c))
            out.write("date >> timing.$JOB_ID\n")
            out.write("mpirun -n {} ./towhee\n".format(c))
            out.write("date >> timing.$JOB_ID\n")
            out.write("cd ../\n")
            out.write("\n")

if __name__ == '__main__':
    cores = sys.argv[1:]

    make_parallel_sims(map(int, cores), 'twh_parallel')
