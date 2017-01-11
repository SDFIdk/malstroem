import numpy as np
import pytest

from malstroem.algorithms import fill, speedups
from data.fixtures import filleddata, fillednoflatsdata, dtmdata

def test_python_fill(dtmdata, filleddata):
    speedups.disable()
    assert not speedups.enabled
    filled = fill.fill_terrain(dtmdata)
    assert np.all(filled >= np.min(dtmdata))
    assert np.max(filled) == np.max(dtmdata)
    assert np.all(filled == filleddata)


def test_python_fill_no_flats(dtmdata, fillednoflatsdata):
    speedups.disable()
    assert not speedups.enabled
    short, diag = fill.minimum_safe_short_and_diag(dtmdata)
    filled = fill.fill_terrain_no_flats(dtmdata, short, diag)
    assert np.all(filled >= np.min(dtmdata))
    assert np.all(filled <= np.max(dtmdata) + (dtmdata.shape[0] + dtmdata.shape[1]) * diag)
    assert np.all(filled == fillednoflatsdata)


def test_optimized_fill(dtmdata, filleddata):
    speedups.enable()
    assert speedups.enabled

    filled = fill.fill_terrain(dtmdata)
    assert np.all(filled >= np.min(dtmdata))
    assert np.max(filled) == np.max(dtmdata)
    assert np.all(filled == filleddata)


def test_optimized_fill_no_flats(dtmdata, fillednoflatsdata):
    speedups.enable()
    assert speedups.enabled
    short, diag = fill.minimum_safe_short_and_diag(dtmdata)
    filled = fill.fill_terrain_no_flats(dtmdata, short, diag)
    assert np.sum(filled > dtmdata) > 0
    assert np.all(filled <= np.max(dtmdata) + (dtmdata.shape[0] + dtmdata.shape[1]) * diag)
    assert np.all(filled == fillednoflatsdata)


def test_compare_fill_python_and_optimized(dtmdata):
    speedups.enable()
    assert speedups.enabled

    filled_optimized = fill.fill_terrain(dtmdata)

    speedups.disable()
    assert not speedups.enabled
    filled_python = fill.fill_terrain(dtmdata)
    assert np.all(filled_optimized==filled_python)


def test_compare_fill_no_flats_python_and_optimized(dtmdata):
    speedups.enable()
    assert speedups.enabled
    short, diag = fill.minimum_safe_short_and_diag(dtmdata)
    filled_optimized = fill.fill_terrain_no_flats(dtmdata, short, diag)
    speedups.disable()
    assert not speedups.enabled
    filled_python = fill.fill_terrain_no_flats(dtmdata, short, diag)

    assert np.all(filled_optimized == filled_python)


def test_minimum_safe_short_and_diag(dtmdata):
    short, diag = fill.minimum_safe_short_and_diag(dtmdata)
    assert diag / short - 2**0.5 < 0.0001


def test_negative_dem_values():
    negative_value = -9999
    dtm = np.empty((10, 10), dtype=np.float32)
    dtm[:, :] = -9999
    dtm[4:6, 4:6] = 0
    short, diag = fill.minimum_safe_short_and_diag(dtm)
    filled = fill.fill_terrain_no_flats(dtm, short, diag)
    assert filled[1, 1] != negative_value
