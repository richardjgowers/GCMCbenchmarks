#!/bin/bash

#$ -N eddie
#$ -cwd
#$ -l h_rt=04:00:00
#$ -l h_vmem=3G

. /etc/profile.d/modules.sh

ulimit -s unlimited 

./DLMONTE-SRL.X
