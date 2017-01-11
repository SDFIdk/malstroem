import numpy as np

from malstroem import dem, io
from data.fixtures import dtmfile, filledfile, flowdirnoflatsfile


def test_dem_processor(tmpdir):
    dem_reader = io.RasterReader(dtmfile)

    tr = dem_reader.transform
    crs = dem_reader.crs

    filled_writer = io.RasterWriter(str(tmpdir.join('filled.tif')), tr, crs)
    flowdir_writer = io.RasterWriter(str(tmpdir.join('flowdir.tif')), tr, crs)
    depths_writer = io.RasterWriter(str(tmpdir.join('depths.tif')), tr, crs)
    accum_writer = io.RasterWriter(str(tmpdir.join('accum.tif')), tr, crs)

    tool = dem.DemTool(dem_reader, filled_writer, flowdir_writer, depths_writer, accum_writer)
    tool.process()

    assert_rasters_are_equal(filledfile, filled_writer.filepath)
    assert_rasters_are_equal(flowdirnoflatsfile, flowdir_writer.filepath)


def assert_rasters_are_equal(file1, file2):
    reader1 = io.RasterReader(file1)
    reader2 = io.RasterReader(file2)

    assert reader1.transform == reader2.transform
    assert reader1.crs == reader2.crs

    data1 = reader1.read()
    data2 = reader2.read()

    assert np.all(data1 == data2), "Files not equal {} != {}".format(file1, file2)