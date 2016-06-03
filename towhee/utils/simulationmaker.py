"""Generates many simulation setups across a range of pressures (isotherms!)

Steps
-----
specify Pressures
for each P:
  calculate chemical potential for that P
  create new directory for that P
  move static files into directory
  fill in template input file with parameters
"""
import os
import shutil
from functools import partial
import numpy as np

from pengrobinson import calc_fugacity_coeff

# More specialised version just for Co2 at 298,
# just have to input P in Pa!
co2_coeff = partial(
    calc_fugacity_coeff,
    T = 298.0,  # K
    Pc = 7.38 * 10 ** 6,  # Pa
    Tc = 304.18,  # K
    omega = 0.22394
)


def make_simulations(sim_name, pressures):
    """
    Parameters
    ----------
    sim_name - prefix for the new directories
    pressures - list of pressures in Pa!

    """
    static_files = [
        'this',
        'that',
    ]
    template = open('towhee_input.template', 'r').read()

    for p in pressures:
        coeff = co2_coeff(p)
        fugacity = p * coeff
        # towhee wants chemical potential in units of K
        chempot = 298.0 * np.log(fugacity)

        newdir = '{}_{}'.format(sim_name, p)
        os.mkdir(newdir)
        for f in static_files:
            shutil.copy(f, os.path.join(newdir, f))
        with open(os.path.join(newdir, 'towhee_input')) as out:
            out.write(template.format(
                chempot=chempot,
                ))
