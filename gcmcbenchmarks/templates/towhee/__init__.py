from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

_FILES = ['qsub.sh', 'towhee_coords', 'towhee_ff_CUSTOM', 'towhee_input']

case1 = {f: _rf(os.path.join('twh_case1', f)) for f in _FILES}
case2 = {f: _rf(os.path.join('twh_case2', f)) for f in _FILES}
case3 = {f: _rf(os.path.join('twh_case3', f)) for f in _FILES}

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
