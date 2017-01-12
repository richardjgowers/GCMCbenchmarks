"""Parsing for towhee results

Assumes towhee output went to stdout, which got saved to '$jobname.o$jobid'

Looks for 'B:' in lines where occurs when the box is reported eg:

Move       Box   Energy [K]  Volume [A^3] Press. [kPa] Molecules
   1100000 B: 1 -0.1123E+07  0.1379E+06          0.0     1  642  <<<< This line

Last number off this line is the number of CO2 molecules

"""

import glob
import numpy as np
import os

from .grab_utils import get_last_ofile

def check_exit(loc):
    pass

def grab_timeseries(loc, ignore_incomplete=False):
    if not ignore_incomplete:
        check_exit(loc)

    ofile = get_last_ofile(loc)

    vals = []
    with open(ofile, 'r') as inf:
        for line in inf:
            # 
            if not 'B:' in line:
                continue
            vals.append(int(line.strip().split()[-1]))
    return np.array(vals, dtype=np.float32) / 8.0  # to mol/uc
