#!/bin/bash

#$ -N twh_{pressure}
#$ -cwd
#$ -l h_rt=06:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

echo "Timing Towhee case 1 at pressure {pressure}" > timing.out
date >> timing.out
./towhee
date >> timing.out
