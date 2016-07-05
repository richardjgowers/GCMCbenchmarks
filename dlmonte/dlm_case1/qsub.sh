#!/bin/bash

#$ -N dlm_{pressure}
#$ -cwd
#$ -l h_rt=06:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh
ulimit -s unlimited

echo "Timing DLMonte case 1 at pressure {pressure}" > timing.out
date >> timing.out
./DLMONTE-SRL.X
date >> timing.out
