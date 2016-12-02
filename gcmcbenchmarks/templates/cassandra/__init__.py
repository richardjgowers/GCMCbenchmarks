from functools import partial
import os
from pkg_resources import resource_filename

_rf = partial(resource_filename, __name__)

# calculated in FugacityCalc notebook
# in kJ/mol
CHEMPOTS = {
    5: -31.7610427,
    10: -30.5636844,
    20: -29.3677046,
    30: -28.6692478,
    40: -28.1744894,
    50: -27.7913478,
    60: -27.4788076,
    70: -27.2149899,
}

_FILES = ['CO2.ff', 'CO2.mcf', 'CO2.pdb',
          'IRMOF.ff', 'IRMOF.mcf', 'IRMOF.pdb', 'IRMOF.xyz',
          'CO2_IRMOF.inp', 'qsub.sh']
# Files found in species2/frag1/
_FRAG1 = ['frag1.dat']
# Files found in species2/fragments
_FRAGMENTS = ['frag_1_1.car', 'frag_1_1.xyz', 'species2_mcf_gen.chk', 'species2_mcf_gen.log',
              'frag_1_1.mcf', 'molecule.pdb', 'species2_mcf_gen.inp']

case1 = {f: _rf(os.path.join('cas_case1', f)) for f in _FILES}
case1['frag1'] = {'frag1.dat': _rf('cas_case1/species2/frag1/frag1.dat')}
case1['fragments'] = {f: _rf(os.path.join('cas_case1/species2/fragments', f))
                      for f in _FRAGMENTS}

case2 = {f: _rf(os.path.join('cas_case2', f)) for f in _FILES}
case2['frag1'] = {'frag1.dat': _rf('cas_case2/species2/frag1/frag1.dat')}
case2['fragments'] = {f: _rf(os.path.join('cas_case2/species2/fragments', f))
                      for f in _FRAGMENTS}

case3 = {f: _rf(os.path.join('cas_case3', f)) for f in _FILES}
case3['frag1'] = {'frag1.dat': _rf('cas_case3/species2/frag1/frag1.dat')}
case3['fragments'] = {f: _rf(os.path.join('cas_case3/species2/fragments', f))
                      for f in _FRAGMENTS}

