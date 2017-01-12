"""Raspa uses cycles not steps

1 cycle = 1 move per molecule

This has functions to convert between moves and cycles for the case studies.

Requires you to know the isotherm a priori..
"""
import glob
import os

# Average number of molecules at a given pressure (ie the result)
# Used to translate between steps and cycles for benchmarking
#
# This changes depending on which case is done, so dict for each
_NMOL_case1 = {  # LJ only
    5 : 4.09 * 8,  # result in mol/uc then *8 because 2x2x2 sim box
    10 : 8.70 * 8,
    20 : 18.57 * 8,
    30 : 30.84 * 8,
    40 : 48.06 * 8,
    50 : 79.01 * 8,
    60 : 115.95 * 8,
    70 : 133.53 * 8,
}
_NMOL_case2 = {  # LJ and FF electrostatics
    5 : 4.26 * 8,
    10 : 9.39 * 8,
    20 : 25.44 * 8,
    30 : 179.30 * 8,
    40 : 185.95 * 8,
    50 : 189.64 * 8,
    60 : 193.60 * 8,
    70 : 194.98 * 8,
}
_NMOL_case3 = {  # LJ and all electrostatics
    5 : 7.66 * 8,
    10 : 16.39 * 8,
    20 : 167.60 * 8,
    30 : 183.32 * 8,
    40 : 190.16 * 8,
    50 : 193.94 * 8,
    60 : 196.35 * 8,
    70 : 198.15 * 8,
}
NMOL = {
    'case1':_NMOL_case1,
    'case2':_NMOL_case2,
    'case3':_NMOL_case3,
}

def steps_to_cycles(steps, case, pressure):
    """Translate a number of steps to cycles

    Parameters
    ----------
    Steps
      Number of Monte Carlo moves desired
    case
      System conditions [case1/case2/case3]
    pressure
      Pressure in kPa

    Returns
    -------
    number of cycles
    """
    # select the pressure->nmol dict to use
    trans = NMOL[case[:5]]

    # need integer number of cycles, minimum of 1
    return max(int(steps / trans[pressure]), 1)


def cycles_to_steps(cycles, case, pressure):
    """Translate a number of cycles to steps

    Parameters
    ----------
    Cycles
      Number of Monte Carlo cycles
    case
      [case1/case2/case3]
    pressure
      pressure in kPa
    """
    trans = NMOL[case[:5]]

    return int(cycles * trans[pressure])


def find_completed_cycles(loc, case, pressure):
    """
    Parameters
    ----------
    loc
      Where the simulation took place (root folder of sim)
    case
      case1/case2/case3
    pressure : int
      pressure in kPa

    Returns
    -------
    number of MC steps
    """
    output = glob.glob(os.path.join(loc, 'Output', 'System_0', '*.data'))[0]
    
    with open(output, 'r') as f:
        # read a chunk from the end of the output
        f.seek(-25000, 2)
        data = f.read()
        
    start = data.find('cycle:') + 6  # where this string ends
    end = data[start:].find('out of') + start
    
    return cycles_to_steps(int(data[start:end]), case, pressure)
