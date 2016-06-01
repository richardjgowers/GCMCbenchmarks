from functools import partial
import os
from pkg_resources import resource_filename

from .conversions import cycles_to_steps, steps_to_cycles, find_completed_steps

_rf = partial(resource_filename, __name__)

_FILES = ['CO2.def', 'force_field.def', 'framework.def', 'IRMOF-1.cif', 'pseudo_atoms.def',
          'simulation.input', 'qsub.sh']

case1 = {f: _rf(os.path.join('rsp_case1', f)) for f in _FILES}
case2 = {f: _rf(os.path.join('rsp_case2', f)) for f in _FILES}
case3 = {f: _rf(os.path.join('rsp_case3', f)) for f in _FILES}

case1_withgrid = {f: _rf(os.path.join('rsp_case1_withgrid', f)) for f in _FILES}
case2_withgrid = {f: _rf(os.path.join('rsp_case2_withgrid', f)) for f in _FILES}
case3_withgrid = {f: _rf(os.path.join('rsp_case3_withgrid', f)) for f in _FILES}
