"""Parse music post processing file

Requires post analysis to have been run (post.ctr)

Strategy for parsing file:
there are 4 sections of '## Per Unitcell Loading'
 1) CO2 in block 1
 2) IRMOF in block 1 (useless)
 3) CO2 in block 2
 4) IRMOF in block 2 (useless)
`rd` is a boolean toggle which turns on (trying) to read values
for every other block
"""

import numpy as np
import os


def grab_timeseries(loc):
    output = os.path.join(loc, 'IRMOF1.CO2.post')

    if not os.path.exists(output):
        raise ValueError("Output not present in {}".format(loc))

    rd = False
    vals = []

    with open(output, 'r') as f:
        for line in f:
            if rd:
                try:
                    val = float(line.split()[1])
                except (ValueError, IndexError):
                    pass
                else:
                    vals.append(val)
            if line.startswith('## Per Unitcell Loading'):
                rd = not rd

    return np.array(vals)
