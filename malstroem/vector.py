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

import json
from osgeo import gdal, ogr


def transform_cell_to_world(cell, geotransform):
    """Transform cell coordinate to world coordinate.

    Parameters
    ----------
    cell : pair of numbers
        A (row, col) pair indicating the specified cell.

    geotransform : list of 6 numbers
        GDAL style of affine transformation parameters.

    Returns
    -------
        Pair of world coordinates (Xworld, Yworld)

    """
    row, col = cell[:2]
    x, y = gdal.ApplyGeoTransform(geotransform, col + 0.5, row + 0.5)
    return (x, y)


def vectorize_labels_file(labeled_file, id_attribute='bspot_id'):
    """Vectorize bluespot id raster

    Parameters
    ----------
    labeled_file : str
        Path to GDAL supported file with bluespot ids (labels)
    id_attribute : str
        Attribute name to write bluespot id to

    Yields
    -------
    feature : dict
        Geojson formatted feature

    """
    src_ds = gdal.Open(labeled_file)
    src_band = src_ds.GetRasterBand(1)

    # Create a memory OGR datasource to put results in.
    mem_drv = ogr.GetDriverByName('Memory')
    mem_ds = mem_drv.CreateDataSource('out')

    mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)

    fd = ogr.FieldDefn(id_attribute, ogr.OFTInteger)
    mem_layer.CreateField(fd)

    # Use 8-connectedness
    options = ['8CONNECTED=8']

    # run the algorithm.
    result = gdal.Polygonize(src_band, src_band.GetMaskBand(), mem_layer, 0, options)
    if result != 0:
        raise Exception('Vectorization failed')

    feat_read = mem_layer.GetNextFeature()
    while feat_read:
        yield json.loads(feat_read.ExportToJson())
        feat_read.Destroy()
        feat_read = mem_layer.GetNextFeature()

    # Without these this code crashes in Python3
    del fd
    del src_ds
    del mem_ds
