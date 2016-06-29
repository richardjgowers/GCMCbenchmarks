# GCMCbenchmarks

Input files for GCMC benchmarking work

List of simulation programs
---------------------------

 - Cassandra v1.1
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

 case1) Only LJ interactions between all components
 case2) As 1) but with fluid-fluid electrostatics
 case3) As 2) but with solid-fluid electrostatics

Creating simulations
--------------------

The input files for simulations can be created using the Python make_* scripts
in this directory.  These all follow the signature::

python make_X.py <case> <destination>

Where case refers to one of the conditions listed above and <destination> refers to the
directory in which they will be made.
