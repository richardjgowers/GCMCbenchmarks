from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

# All files in a dlmonte simulation
_FILES = ['CONTROL', 'FIELD', 'CONFIG', 'qsub.sh']

# For each case, a dict of filename to filepath
case1 = {f: _rf(os.path.join('dlm_case1', f)) for f in _FILES}
case2 = {f: _rf(os.path.join('dlm_case2', f)) for f in _FILES}
case3 = {f: _rf(os.path.join('dlm_case3', f)) for f in _FILES}


