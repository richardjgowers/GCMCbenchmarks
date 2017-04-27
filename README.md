# GCMCbenchmarks

Input files for GCMC benchmarking work

List of simulation programs
---------------------------

 - Cassandra v1.2
 - DL_Monte2 v2.0.1-2016_May-Beta
 - Music v4.0
 - RASPA v2.0
 - Towhee v7.1.0


System details
--------------

2 x 2 x 2 unit cell of IRMOF-1 adsorbent (8 x 424 atoms (3392))

CO2 adsorbate


System conditions
-----------------

Temperature 208.0 K


3 sets of simulations were performed with all software

 - Setup 1: Only LJ interactions between all components
 - Setup 2: As 1) but with fluid-fluid electrostatics
 - Setup 3: As 2) but with solid-fluid electrostatics

Creating simulations
--------------------

The input files for simulations can be created using the Python `make_*` scripts
in this directory.  The following scripts are available::

 * `make_cassandra_sims.py`
 * `make_dlm_sims.py`
 * `make_music_sims.py`
 * `make_raspa_sims.py`
 * `make_towhee_sims.py`

These generally follow the signature `make_X_sims.py <setup> <destination>` where `<setup>` refers to one of the conditions listed above and `<destination>` refers to the
directory in which they will be made.

For example:

`make_raspa_sims.py setup2 rsp_sims_setup2 -n 10000000`

Makes a set of Raspa simulations for all pressures in the directory "`rsp_sims_setup2`",
with a length of 10M steps.

Full details of the available options are detailed in the `-h` option for each script.
