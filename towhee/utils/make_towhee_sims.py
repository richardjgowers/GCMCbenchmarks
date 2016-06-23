#!/usr/bin/env python
"""Make a set of Towhee simulations

"""
from __future__ import division

import sys
import os
import shutil

# pressures in kPa to run
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]

# chemical potentials calculated in PREoS notebook
CHEMPOTS = {5:-3819.9767,
			10:-3675.9676,
			20:-3532.1242,
			30:-3448.1191,
			40:-3388.6133,
			50:-3342.5320,
			60:-3304.9420,
			70:-3273.2120,
			}

def make_sims(pressure_values, prefix):
	for p in PRESSURES:
		newdir = 'twh_{}'.format(p)
		os.mkdir(newdir)

		for f in ['towhee_coords', 'towhee_ff_CUSTOM']:
			shutil.copy(os.path.join(prefix, f),
						os.path.join(newdir, f))

		template = open(os.path.join(prefix, 'towhee_input'), 'r').read()
		with open(os.path.join(newdir, 'towhee_input'), 'w') as out:
			out.write(template.format(chempot=CHEMPOTS[p]))


if __name__ == '__main__':
	try:
		prefix = sys.argv[1]
	except IndexError:
		raise SystemExit("Usage: {} templatedir".format(sys.argv[0]))
	else:
		make_sims(PRESSURES, prefix)
