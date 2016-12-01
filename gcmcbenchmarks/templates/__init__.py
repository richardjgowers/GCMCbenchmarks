from . import cassandra
from . import dlmonte
from . import music
from . import raspa
from . import towhee

# possible pressures in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]

# string used for docopt & command line interface for making simulations
makestr = \
"""
Usage:
  make_*_sim <case> <dir> [-n NSTEPS -s NSAMP -c NCOORD] [(-p <pressures>...)]

Options:
  -h --help
  -v --version
  -n N                Number of steps [default: 10000000]
  -s N                Number of steps between samples [default: 1000]
  -c N                Number of steps between saving coordinatse [default: 100000]
  -p                  Specify manual pressure points
  <pressures>...      Pressure points [default: 1 2 3]

"""
