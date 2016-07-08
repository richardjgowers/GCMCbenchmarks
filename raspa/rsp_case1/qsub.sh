#!/bin/bash

#$ -N rsp_{pressure}
#$ -cwd
#$ -l h_rt=12:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

# Ensure that RASPA is linked in parent directory!
export RASPA_DIR=../RASPA/

echo "Timing DLMonte case 1 at pressure {pressure}" > timing.out
date >> timing.out
./simulate simulation.input
date >> timing.out
