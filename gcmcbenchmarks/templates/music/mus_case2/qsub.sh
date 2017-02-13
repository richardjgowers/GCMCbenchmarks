#!/bin/bash
#$ -R y
#$-l h_vmem=1G
#$ -l h_rt=20:00:00
#$ -j y
#$ -N mus_c2_{pressure}
#$ -cwd
#$ -V

. /etc/profile.d/modules.sh
ulimit -s unlimited

cat /proc/cpuinfo > cpuinfo.{pressure}

source setpath

echo "Timing Music case 2 at {pressure}" > timing.$JOB_ID
date >> timing.$JOB_ID
./music_gcmc_4.exe gcmc.ctr >& gcmc.log
date >> timing.$JOB_ID



