"""Make all simulations

creates many directories with input files

prefix
cas - Cassandra
dlm - DL Monte
mus - Music
rsp - Raspa
twh - Towhee


"""
import sys

import make_towhee_sims
import make_dlm_sims


# Pressures to run in kPa
PRESSURES = [5, 10, 20, 30, 40, 50, 60, 70]


def make_all_sims(pressures, suffix):
    """Make all simulation directories for all programs

    """
    make_dlm_sims.make_sims(pressures, suffix)
    make_towhee_sims.make_sims(pressures, suffix)


if __name__ == '__main__':
    try:
        suffix = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage: {} templatesuffix".format(sys.argv[0]))
    else:
        make_all_sims(PRESSURES, suffix)
