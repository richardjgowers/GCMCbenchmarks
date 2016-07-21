#!/bin/bash

#$ -N twh_{pressure}
#$ -cwd
#$ -l h_rt=06:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

echo "Timing Towhee case 1 at pressure {pressure}" > timing.$JOB_ID
date >> timing.$JOB_ID
./towhee
date >> timing.$JOB_ID
