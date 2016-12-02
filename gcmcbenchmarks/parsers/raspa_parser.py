import glob
import numpy as np
import os


def grab_timeseries(loc):
    """Grab timeseries including equilibration time"""
    def _getval1(l):
        #return l
        return float(l.split('adsorption:')[1].split('(avg.')[0])
        #return float(l.split('avg.')[1].split(')')[0])
    def _getval2(l):
        return float(l.split('adsorption:')[1].split('[mol')[0])

    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]    

    vals = []
    for line in open(output, 'r'):
        if line.lstrip(' \t').startswith('absolute adsorption'):
            if 'avg.' in line:
                vals.append(_getval1(line.lstrip()))
            else:
                vals.append(_getval2(line.lstrip()))
    return np.array(vals)
