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
from __future__ import division
import cython
import numpy as np
from ._definitions cimport DTYPE_t_FILL, DTYPE_t_DTM, DTYPE_t_FILLNOFLAT
cimport numpy as np


cdef inline DTYPE_t_FILL fill_float_max(DTYPE_t_FILL a, DTYPE_t_FILL b): return a if a >= b else b
cdef inline DTYPE_t_FILL fill_float_min(DTYPE_t_FILL a, DTYPE_t_FILL b): return a if a <= b else b

cdef inline DTYPE_t_FILLNOFLAT fillnoflat_float_max(DTYPE_t_FILLNOFLAT a, DTYPE_t_FILLNOFLAT b): return a if a >= b else b
cdef inline DTYPE_t_FILLNOFLAT fillnoflat_float_min(DTYPE_t_FILLNOFLAT a, DTYPE_t_FILLNOFLAT b): return a if a <= b else b

cimport cython
@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
def _fill_terrain(np.ndarray[DTYPE_t_FILL, ndim=2] dtm not None, np.ndarray[DTYPE_t_FILL, ndim=2] filled not None, unsigned int fromrow, unsigned int torow, unsigned int fromcol, unsigned int tocol):
    if fromrow == torow or fromcol == tocol:
        raise ValueError('Width or height of processing area is zero')
    cdef int rowstep = 1 if torow > fromrow else -1
    cdef int colstep = 1 if tocol > fromcol else -1

    cdef DTYPE_t_FILL filled_value, dtm_value, min_value, new_value
    cdef unsigned int up, down, left, right, row, col

    cdef int changes = 0
    row = fromrow
    while row != torow:
        up = <unsigned int>(row - 1)
        down = <unsigned int>(row + 1)
        col = fromcol
        while col != tocol:
            filled_value = filled[row,col]
            dtm_value = dtm[row, col]
            if(filled_value > dtm_value):
                left = <unsigned int>(col - 1)
                right = <unsigned int>(col + 1)

                min_value = filled_value
                min_value = fill_float_min( filled[  up, left],  min_value )
                min_value = fill_float_min( filled[  up, col],   min_value )
                min_value = fill_float_min( filled[  up, right], min_value )
                min_value = fill_float_min( filled[ row, left],  min_value )
                min_value = fill_float_min( filled[ row, right], min_value )
                min_value = fill_float_min( filled[down, left],  min_value )
                min_value = fill_float_min( filled[down, col],   min_value )
                min_value = fill_float_min( filled[down, right], min_value )

                # Cannot be lower than terrain
                new_value = fill_float_max(min_value, dtm_value)
                if( new_value != filled_value):
                    filled[row, col] = new_value
                    changes += 1
            col += colstep
        row += rowstep

    return changes

@cython.boundscheck(False) # turn of bounds-checking for entire function
@cython.wraparound(False)
def _fill_terrain_no_flats(np.ndarray[DTYPE_t_DTM, ndim=2] dtm not None, np.ndarray[DTYPE_t_FILLNOFLAT, ndim=2] filled not None, unsigned int fromrow, unsigned int torow, unsigned int fromcol, unsigned int tocol, DTYPE_t_FILLNOFLAT short, DTYPE_t_FILLNOFLAT diag):
    if fromrow == torow or fromcol == tocol:
        raise ValueError('Width or height of processing area is zero')
    cdef int rowstep = 1 if torow > fromrow else -1
    cdef int colstep = 1 if tocol > fromcol else -1

    cdef DTYPE_t_FILLNOFLAT filled_value, dtm_value, min_value, new_value
    cdef unsigned int up, down, left, right, row, col

    cdef int changes = 0
    row = fromrow
    while row != torow:
        up = <unsigned int>(row - 1)
        down = <unsigned int>(row + 1)
        col = fromcol
        while col != tocol:
            filled_value = filled[row,col]
            dtm_value = dtm[row, col]
            if filled_value > dtm_value:
                left = <unsigned int>(col - 1)
                right = <unsigned int>(col + 1)

    #min_value = filled_value
    #min_value = min( filled[  up, left]  + diag,  min_value )
    #min_value = min( filled[  up, col]   + short,   min_value )
    #min_value = min( filled[  up, right] + diag, min_value )
    #min_value = min( filled[ row, left]  + short,  min_value )
    #min_value = min( filled[ row, right] + short, min_value )
    #min_value = min( filled[down, left]  + diag,  min_value )
    #min_value = min( filled[down, col]   + short,   min_value )
    #min_value = min( filled[down, right] + diag, min_value )

                # Do essentially the same as above, but with fewer assignments and additions
                min_value = fillnoflat_float_min(filled[  up, left],
                                fillnoflat_float_min(filled[  up, right],
                                    fillnoflat_float_min( filled[down, left], filled[down, right]))) + diag
                min_value = fillnoflat_float_min(min_value,
                                fillnoflat_float_min(filled[  up, col],
                                    fillnoflat_float_min( filled[ row, left],
                                        fillnoflat_float_min( filled[ row, right], filled[down, col]))) + short)
                min_value = fillnoflat_float_min(min_value, filled_value)

                # Cannot be lower than terrain
                new_value = fillnoflat_float_max(min_value, dtm_value)
                if new_value != filled_value:
                    filled[row, col] = new_value
                    changes += 1
            col += colstep
        row += rowstep

    return changes
