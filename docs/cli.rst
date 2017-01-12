========================
Command Line Users Guide
========================
malstroem's command line is a single program named ``malstroem`` which has a number og subcommands. Each subcommand
exposes a malstroem process.

Available subcommands can be seen by invoking ``malstroem --help``

.. code-block:: console

    $ malstroem --help
    Usage: malstroem [OPTIONS] COMMAND [ARGS]...

      Calculate simple hydrologic models.

      To create rainfall scenarios use either the sub command 'complete' or the
      following sequence of sub command calls: filled, depths, flowdir, bspots,
      wsheds, pourpts, network, rain.

      To get help for a sub command use: malstroem subcommand --help

      Examples:
      malstroem complete -r 10 -r 30 -filter 'volume > 2.5' -dem dem.tif -outdir ./outdir/
      malstroem filled -dem dem.tif -out filled.tif

    Options:
      --version            Show the version and exit.
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.

    Commands:
      accum     Calculate accumulated flow.
      bspots    Label bluespots.
      complete  Quick option to complete process.
      depths    Calculate bluespot depths.
      filled    Create a filled (depressionless) DEM.
      flowdir   Calculate surface water flow directions.
      network   Calculate stream network between bluespots.
      pourpts   Determine pour points.
      rain      Calculate bluespot fill and spill volumes for...
      wsheds    Calculate bluespot watersheds.

Help for a given subcommand is available by invoking ``malstroem subcommand --help``. For example:

.. code-block:: console

    $ malstroem accum --help
    Usage: malstroem accum [OPTIONS]

      Calculate accumulated flow.

      The value in an output cell is the total number of cells upstream of that
      cell. To get the upstream area multiply with cell size.

    Options:
      -flowdir PATH        Flow direction file  [required]
      -out PATH            Output file (accumulated flow)  [required]
      -v, --verbosity LVL  Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help               Show this message and exit.

General considerations
----------------------
malstroem makes the following assumptions reagarding the input

 * DEM horisontal and vertical units are meters.
 * All subsequent processing steps assume input data as output by the former processing step of malstroem.

malstroems generally does not do very much checking that input makes sense together.

Vector output options
---------------------
malstroem uses `OGR <http://www.gdal.org>`_ for writing vector data. Output vector data can be tweaked using OGR
specific parameters `format`, `lco`, and `dsco`.

Example writing to `GeoPackage format <http://www.gdal.org/drv_geopackage.html>`_ from ``malstroem pourpts``:

.. code-block:: console

    $ malstroem pourpts -bluespots labeled.tif -depths depths.tif -watersheds wsheds.tif -dem dem.tif -format gpkg -out dbfile.gpkg -layername pourpoints

For documentation of OGR features see the documentation of
`OGR formats <http://www.gdal.org/ogr_formats.html>`_.

Raster output options
---------------------
malstroem uses `GDAL <http://www.gdal.org>`_ for writing raster data. All raster data are written in
`GeoTiff <http://www.gdal.org/frmt_gtiff.html>`_ format.

malstroem complete
------------------
The ``complete`` subcommand gives you fast-track processing from input DEM to output rain incidents including most
intermediate datasets. It basically collects the subcommands ``filled``, ``depths``, ``flowdir``, ``accum``,
``bspots``, ``wsheds``, ``pourpts``, ``network`` and ``rain`` into one single subcommand. See these subcommands to learn
more about what happens or see `Complete chain of processes`_.

Arguments:
 * ``dem`` is a raster digital elevation model. Both horisontal and vertical units must be meters.
 * ``r`` or ``rain`` One or more rain incidents to calculate. In mm. ``-r value`` can be specified multiple times.
 * If ``accum`` is specified the accumulated flow is calculated. This takes some time and is not strictly required.
 * If ``vector`` is specified the bluespots and watersheds are vectorized. This takes some time and is not required.
 * ``filter`` allows ignoring bluespots based on their area, maximum depth and volume.
   Format: ``area > 20.5 and (maxdepth > 0.05 or volume > 2.5)``.
   Bluespots that do not pass the filter are ignored in all subsequent calculations. For instance their capacity is
   not taken into account.
 * ``outdir`` is the path to the output directory where all output files are written. This directory must exist and be
   empty.

Example:

.. code-block:: console

    $ malstroem complete -r 10 -r 30 -filter 'volume > 2.5' -dem dem.tif -outdir ./outdir/

malstroem filled
----------------
The ``filled`` subcommand creates a filled (depressionless) DEM.

In a depressionless terrain model each cell will have at least one non-uphill path to the raster edge. This means that
a depressionless terrain model will have flat areas where it has been filled.

Arguments:
 * ``dem`` is a raster digital elevation model. Both horisontal and vertical units must be meters.

Outputs:
 * The filled DEM to a new raster

Example:

.. code-block:: console

    $ malstroem filled -dem dem.tif -out filled.tif

malstroem depths
----------------
The ``depths`` subcommand calculates bluespot depths.

Depths are calculated by subtracting the original DEM from the filled DEM

Arguments:
 * ``dem`` is the raster digital elevation model.
 * ``filled`` is the filled version of the input DEM.

Outputs:
 * A new raster with the bluespot depth in each cell. Cells not in a bluespot will have the value 0.

Example:

.. code-block:: console

    $ malstroem depths -dem dem.tif -filled filled.tif -out depths.tif

malstroem flowdir
-----------------
The ``flowdir`` subcommand calculates surface water flow directions.

This is a two step process:

Step 1:
    Fill depressions in the DEM in a way which preserves a downward slope along the flow path. This is done by requiring
    a (very) small minimum slope between cells. This results in flow over filled areas being routed to the nearest pour
    point.

Step 2:
    Flow directions for each cell. Uses a D8 flow routing algorithm: At each cell the slope to each of the 8 neighboring
    cells is calculated. The flow is routed to the cell which has the steepest slope. If multiple cells share the same maximum
    slope the algorithm picks one of these cells.

Flow direction from a cell is encoded: `Up=0`, `UpRight=1`, ..., `UpLeft=7`, `NoDirection=8`

Arguments:
 * ``dem`` is the raster digital elevation model.

Outputs:
 * A new raster where the flow direction from each cell is encoded.

Example:

.. code-block:: console

    $ malstroem depths -dem dem.tif -out flowdir.tif

malstroem accum
---------------
The subcommand ``accum`` calculates accumulated flow.

The value in an output cell is the total number of cells upstream of that cell.

Arguments:
 * ``flowdir`` is the flow direction raster.

Outputs:
 * A raster where the value in each cell is the number of cells upstream of that cell.

Example:

.. code-block:: console

    $ malstroem accum -flowdir flowdir.tif -out out.tif

malstroem bspots
----------------
The ``bspots`` subcommand identifies and labels all cells belonging to each bluespot with a unique bluespot ID.

.. note::

    * The unique ID is an integer in the range from 1 to the number of bluespots in the dataset. So bluespot IDs are
      NOT unique across different datasets.
    * IDs are not necessarily assigned the same way between different runs on the same dataset.
    * The ID 0 (zero) is used for cells which do not belong to a bluespot.

Bluespots with certain properties can be ignored by specifying a filter expression. Available properties are

``maxdepth`` which is the maximum depth of the bluespot.
``area`` which is the area of the bluespot in m2.
``volume`` which is the bluespot volume (or water capacity) in m3.

Allowed operators are ``<``, ``>``, ``==``, ``!=``, ``>=``, ``<=``, ``and`` and ``or``. Parenthises can be used to make
the expression more readable.

An example of a valid `filter`:

.. code-block:: python

    maxdepth > 0.05 and (area > 20 or volume > 0.5)

.. note::

    * Bluespots that do not pass the filter are ignored in all subsequent calculations. For instance their capacity is
      not taken into account.


Arguments:
 * ``depths`` is a raster with bluespot depths
 * ``filter`` allows ignoring bluespots based on their area, maximum depth and volume.
   Format: ``area > 20.5 and (maxdepth > 0.05 or volume > 2.5)``.
   Bluespots that do not pass the filter are ignored in all subsequent calculations. For instance their capacity is
   not taken into account.`

Outputs:
 * A raster with bluespot IDs. The ID 0 (zero) is used for cells which do not belong to a bluespot.

Example:

.. code-block:: console

    $ malstroem bspots -depths depths.tif -filter "maxdepth > 0.05 and (area > 20 or volume > 0.5)" -out labeled.tif

malstroem wsheds
----------------
The subcommand ``wsheds`` determines the local watershed of each bluespot.

All cells in the local watershed is assigned the bluespot ID.

Arguments:
 * ``bluespots`` is the bluespot ID raster.
 * ``flowdir`` is the flow direction raster.

Outputs:
 * A raster with bluespot watersheds identified by bluespot ID.

Example:

.. code-block:: console

    $ malstroem wshed -bluespots labeled.tif -flowdir flowdir.tif -out wsheds.tif

malstroem pourpts
-----------------
The ``pourpts`` subcommand determines a pour point for each bluespot.

A pour point is the point where water leaves the blue spot when it is filled to its maximum capacity.

Pour point are determined using one of two methods:

 * Random candidate. Requires DEM only
 * Maximum accumulated flow candidate. Requires accumulated flow

The output of the two methods only differ when there are more than one pour point candidate (ie multiple threshold
cells with identical Z for a given bluespot).

Arguments:
 * ``bluespots`` is the bluespot ID raster.
 * ``depths`` is a raster with bluespot depths.
 * ``watersheds`` is a raster with local bluespot watershed identified by bluespot IDs.
 * ``dem`` the DEM. Only required if ``accum`` is not used.
 * ``accum`` accumulated flow raster. Required if ``dem`` is not used.
 * ``out`` output OGR datasource.
 * ``layername`` name of output vector layer within the output datasource.

Outputs:
 * Vector Point layer with pour points.

.. list-table:: **Pour point attributes**
   :header-rows: 1

   * - Attribute Name
     - Description
   * - bspot_id
     - Bluespot ID
   * - bspot_area
     - Bluespot area in m2
   * - bspot_vol
     - Bluespot volume (or capacity) in m3
   * - bspot_dmax
     - Maximum depth of the bluespot
   * - bspot_fumm
     - Rain needed to fill up this bluespot with water from local watershed only. In mm.
   * - wshed_area
     - Area of local bluespot watershed. In m2.
   * - cell_row
     - Raster row index of pour point location
   * - cell_col
     - Raster column index of pour point location


Example:

.. code-block:: console

    $ malstroem pourpts -bluespots labeled.tif -depths depths.tif -watersheds wsheds.tif -dem dem.tif -out shpdir/ -layername pourpoints

malstroem network
-----------------
The subcommand ``network`` calculates the stream network between bluespots.

Streams are traced from the pour point of each bluespot using the flow directions raster.

A stream ends:
 * when it first enters the next downstream bluespot.
 * when it merges with another stream

When two or more streams merge a new node of type ``junction`` is inserted and a new stream is traced downstream
from the node.

Streams stop at the border of the bluespot because routing within the bluespot will otherwise happen on a synthetic
surface sloping towards the pour point. This has nothing to do with the real flow of the water.

Arguments:
 * ``bluespots`` bluespots ID raster.
 * ``flowdir`` flow direction raster.
 * ``pourpoints`` OGR vector datasource with pour points.
 * ``pourpoints_layer`` layer name within `pourpoints` datasource. Needed when datasource can have multiple layers (eg.
   a database).
 * ``out`` output OGR datasource.
 * ``out_nodes_layer`` layer name for output `nodes` layer within the output datasource.
 * ``out_streams_layer`` layer name for output `streams` layer within the output datasource

Outputs:
 * Nodes vector Point layer establishing a network
 * Streams vector LineString layer

.. list-table:: **Nodes attributes**
   :header-rows: 1

   * - Attribute Name
     - Description
   * - nodeid
     - Integer ID for each node.
   * - nodetype
     - ``pourpoint`` or ``junction``.
   * - dstrnodeid
     - ``nodeid`` of the next downstream node.
   * - bspot_id
     - Bluespot ID. NULL for nodes of type ``junction``.
   * - bspot_area
     - Bluespot area in m2. 0 (zero) for nodes of type ``junction``.
   * - bspot_vol
     - Bluespot volume (or capacity) in m3. 0 (zero) for nodes of type ``junction``.
   * - wshed_area
     - Area of local bluespot watershed. In m2. 0 (zero) for nodes of type ``junction``.
   * - cell_row
     - Raster row index of pour point location
   * - cell_col
     - Raster column index of pour point location

.. list-table:: **Streams attributes**
   :header-rows: 1

   * - Attribute Name
     - Description
   * - nodeid
     - Integer ID for starting node of the stream.
   * - dstrnodeid
     - ``nodeid`` of the next downstream node.

.. note::

    * As streams end at the border of the downstream bluespot they do not form a complete geometric network.
    * The network can be established by using the ``nodeid`` and ``dstrnodeid`` attributes.

Example:

.. code-block:: console

    $ malstroem network -bluespots labeled.tif -flowdir flowdir.tif -pourpoints shpdir/pourpoints.shp -out shpdir/ -out_nodes_layer nodes -out_streams_layer streams

malstroem rain
--------------
The subcommand ``rain`` calculates bluespot fill and spill volumes for specific rain events.

For each rain event bluespot fill and spill volumes are calculated for all nodes and spill is propagated downstream.

Arguments:
 * ``nodes`` OGR datasource containing nodes layer.
 * ``nodes_layer`` layer name within `nodes` datasource. Needed when datasource can have multiple layers (eg. a database).
 * ``r`` or ``rain`` is a rain incident in mm. Note that multiple rain incidents can be calculated at once by repeating
   the '-r' option.
 * ``out`` output OGR datasource.
 * ``out_layer`` layer name for output layer within the output datasource.

Outputs:
 * Events Point layer where fill and spill has been calculated for all nodes

.. list-table:: **Events attributes**
   :header-rows: 1

   * - Attribute Name
     - Description
   * - nodeid
     - Integer ID for each node.
   * - nodetype
     - ``pourpoint`` or ``junction``.
   * - dstrnodeid
     - ``nodeid`` of the next downstream node.
   * - bspot_id
     - Bluespot ID. NULL for nodes of type ``junction``.
   * - bspot_area
     - Bluespot area in m2. 0 (zero) for nodes of type ``junction``.
   * - bspot_vol
     - Bluespot volume (or capacity) in m3. 0 (zero) for nodes of type ``junction``.
   * - wshed_area
     - Area of local bluespot watershed. In m2. 0 (zero) for nodes of type ``junction``.
   * - cell_row
     - Raster row index of pour point location
   * - cell_col
     - Raster column index of pour point location

.. list-table:: **Events attributes repeated for each rain event of xx mm**
   :header-rows: 1

   * - Attribute Name
     - Description
   * - rainv_xx
     - Volume of rain falling on the local watershed. In m3.
   * - v_xx
     - Volume of water in the bluespot. (Sum of water falling on local watershed and water flowing in from upstream).
       In m3.
   * - pctv_xx
     - Percentage of bluespot volume (capacity) filled.
   * - spillv_xx
     - Volume of water spilled downstream from the bluespot. In m3.


Example:

.. code-block:: console

    $ malstroem rain -nodes shpdir/ -nodes_layer nodes -r 10 -r 20 -out shpdir/ -out_layer nodes


Complete chain of processes
---------------------------
The complete process from DEM to fill and spill volumes for a rain event can be calculated with the
``malstroem complete`` subcommand (see `malstroem complete`_). If you need greater control than offered by this command, you need to do the
processing in steps using the other subcommands.

The below series of process calls will produce the same results as ``malstroem complete``:

.. code-block:: console

    $ malstroem filled -dem dem.tif -out filled.tif
    $ malstroem depths -dem dem.tif -filled filled.tif -out depths.tif
    $ malstroem flowdir -dem dem.tif -out flowdir.tif
    $ malstroem accum -flowdir flowdir.tif -out accum.tif
    $ malstroem bspots -filter "maxdepth > 0.05 and (area > 20 or volume > 0.5)" -depths depths.tif -out bspots.tif
    $ malstroem wsheds -bluespots bspots.tif -flowdir flowdir.tif -out wsheds.tif
    $ malstroem pourpts -bluespots bspots.tif -depths depths.tif -watersheds wsheds.tif -dem dem.tif -out shpdir/
    $ malstroem network -bluespots bspots.tif -flowdir flowdir.tif -pourpoints shpdir/ -out shpdir
    $ malstroem rain -nodes shpdir/ -r 10 -r 20 -out shpdir/

This workflow utilizes default OGR output format and layer names. Both formats and layer names can be controlled by
parameters.