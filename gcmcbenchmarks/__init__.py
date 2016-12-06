__version__ = '0.0.1'


from . import templates
from . import parsers

# Fill top namespace
from .parsers.general_parser import (
    find_simdirs,
    find_equil,
    grab_all_results,
    parse,
)
from .parsers.time_parser import (
    parse_timefile,
    parse_cpuinfo,
    get_times,
)
