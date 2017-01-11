# coding=utf-8
# -------------------------------------------------------------------------------------------------
# Copyright (c) 2016
# Developed by Septima.dk and Thomas Balstrøm (University of Copenhagen) for the Danish Agency for
# Data Supply and Efficiency. This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free Software Foundation,
# either version 2 of the License, or (at you option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PORPOSE. See the GNU Gene-
# ral Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not,
# see http://www.gnu.org/licenses/.
# -------------------------------------------------------------------------------------------------
from __future__ import (absolute_import, division, print_function) #, unicode_literals)
from builtins import *

import click
import click_log

from malstroem import io
from malstroem.algorithms import fill, flow

NODATASUBST = -999

@click.command('filled')
@click.option('-dem', required=True, type=click.Path(exists=True), help='DEM file')
@click.option('-out', required=True, type=click.Path(exists=False), help='Output file (filled DEM)')
@click_log.simple_verbosity_option()
def process_filled(dem, out):
    """Create a filled (depressionless) DEM.
    """
    dem_reader = io.RasterReader(dem, nodatasubst=NODATASUBST)
    filled_writer = io.RasterWriter(out, dem_reader.transform, dem_reader.crs, NODATASUBST)

    filled_data = fill.fill_terrain(dem_reader.read())
    filled_writer.write(filled_data)

@click.command('depths')
@click.option('-dem', required=True, type=click.Path(exists=True), help='DEM file')
@click.option('-filled', required=True, type=click.Path(exists=True), help='Filled DEM file')
@click.option('-out', required=True, type=click.Path(exists=False), help='Output file (depths)')
@click_log.simple_verbosity_option()
def process_depths(dem, filled, out):
    """Calculate bluespot depths.

    Depths are calculated by subtracting the original DEM from the filled DEM
    """
    dem_reader = io.RasterReader(dem, nodatasubst=NODATASUBST)
    filled_reader = io.RasterReader(filled, nodatasubst=NODATASUBST)
    depths_writer = io.RasterWriter(out, dem_reader.transform, dem_reader.crs, NODATASUBST)

    depths_data = filled_reader.read() - dem_reader.read()

    depths_writer.write(depths_data)


@click.command('flowdir')
@click.option('-dem', required=True, type=click.Path(exists=True), help='DEM file')
@click.option('-out', required=True, type=click.Path(exists=False), help='Output file (flow directions)')
@click_log.simple_verbosity_option()
def process_flowdir(dem, out):
    """Calculate surface water flow directions.

    This is a two step process:
    
    Step 1:
    Fill depressions in the DEM in a way which preserves a downward slope along the flow path. This is done by requiring
    a (very) small minimum slope between cells. This results in flow over filled areas being routed to the nearest pour
    point.

    Step 2:
    Flow directions for each cell. Uses a D8 flow routing algorithm: At each cell the slope to each of the 8 neighboring
    cells is calculated. The flow is routed to the cell which has the steepest slope. If multiple cells share the same maximum
    slope the algorithm picks one of these cells.

    Flow direction from a cell is encoded: Up=0, UpRight=1, ..., UpLeft=7, NoDirection=8
    """
    dem_reader = io.RasterReader(dem, nodatasubst=NODATASUBST)
    flowdir_writer = io.RasterWriter(out, dem_reader.transform, dem_reader.crs, NODATASUBST)

    dem_data = dem_reader.read()
    short, diag = fill.minimum_safe_short_and_diag(dem_data)
    filled_no_flats = fill.fill_terrain_no_flats(dem_data, short=short, diag=diag)
    del dem_data

    flowdir_data = flow.terrain_flowdirection(filled_no_flats, edges_flow_outward=True)

    flowdir_writer.write(flowdir_data)

@click.command('accum')
@click.option('-flowdir', required=True, type=click.Path(exists=True), help='Flow direction file')
@click.option('-out', required=True, type=click.Path(exists=False), help='Output file (accumulated flow)')
@click_log.simple_verbosity_option()
def process_accum(flowdir, out):
    """Calculate accumulated flow.

    The value in an output cell is the total number of cells upstream of that cell. To get the upstream area
    multiply with cell size.
    """
    flowdir_reader = io.RasterReader(flowdir)
    accum_writer = io.RasterWriter(out, flowdir_reader.transform, flowdir_reader.crs)

    flowdir_data = flowdir_reader.read()
    accum_data = flow.accumulated_flow(flowdir_data)

    accum_writer.write(accum_data)