import glob
import numpy as np
import os


def check_exit(loc):
    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]

    if not os.path.exists(output):
        raise ValueError("Output not present in dir: {}".format(loc))
    with open(output, 'r') as f:
        f.seek(-100, 2)  # seek to before EOF
        if not 'Simulation finished' in f.read():
            raise ValueError("Output didn't exit correctly in dir: {}".format(loc))

    return True

def grab_timeseries(loc, ignore_incomplete=False):
    """Grab timeseries including equilibration time"""
    def _getval1(l):
        #return l
        return float(l.split('adsorption:')[1].split('(avg.')[0])
        #return float(l.split('avg.')[1].split(')')[0])
    def _getval2(l):
        return float(l.split('adsorption:')[1].split('[mol')[0])

    if not ignore_incomplete:
        check_exit(loc)

    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]

    vals = []
    with open(output, 'r') as f:
        for line in f:
            if line.lstrip(' \t').startswith('absolute adsorption'):
                if 'avg.' in line:
                    vals.append(_getval1(line.lstrip()))
                else:
                    vals.append(_getval2(line.lstrip()))
    return np.array(vals)
