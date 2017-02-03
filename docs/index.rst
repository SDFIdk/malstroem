.. malstroem documentation master file, created by
   sphinx-quickstart on Wed Jan  4 13:07:28 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============================================================================
malstroem
============================================================================
Tools for screening of bluespots and water flow between bluespots

Features
--------
malstroem provides command line tools and a python api to calculate:

* Depressionless (filled, hydrologically conditioned) elevation models
* Surface flow directions
* Accumulated flow
* Blue spots
* Local watershed for each bluespot
* Pour points (point where water leaves blue spot when it is filled to its maximum capacity)
* Flow paths between blue spots
* Fill volume at specified rain incidents
* Spill over between blue spots at specified homogeneous rain incidents

Assumptions
-----------
malstroem makes some assumptions to simplify calculations. The most important ones which you must be aware of:

.. note::

    * malstroem assumes that the terrain is an impermeable surface. This may change in a later version.
    * malstroem does not know the concept of time. This means that the capacity of surface streams is infinite no matter
      the width or depth. Streams won´t flow over along their sides. The end result is the situation after infinite time,
      when all water has reached its final destination.
    * Water flows from one cell to one other neighbour cell (the D8 method).
    * The DEM used must cover an entire drainage basin (or more basins) in order to estimate correct stream flows from
      all upstream sub-watersheds within the basins.

Example usage
-------------
Calculate all derived data including vectorization of bluespot, wateshed and streams rasters for 10mm and 30mm rain
incidents ignoring bluespots where the maximum water depth is less than 5cm:

.. code-block:: console

   malstroem complete -r 10 -r 30 -filter "maxdepth > 0.5" -vector -dem dem.tif -outdir c:\outputdirectory

The project
-----------
.. toctree::
   :maxdepth: 2

   about


Installation
------------
.. toctree::
   :maxdepth: 2

   installation

Command line interface
----------------------
.. toctree::
   :maxdepth: 2

   cli

API documentation
-----------------
.. toctree::
   :maxdepth: 2

   api/malstroem




Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
