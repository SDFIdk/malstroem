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


def check_filter(filter):
    # TODO: Stupid check mechanism. Could be done better
    allowed_words = ['area', 'maxdepth', 'volume', 'and', 'or']
    allowedchars = '<>=!0123456789.()'
    for w in allowed_words:
        filter = filter.replace(w, '')
    for c in allowedchars:
        filter = filter.replace(c, '')
    filter = filter.strip()
    if filter:
        raise Exception('Unsupported filter statement. Illegal parts: {}'.format(filter))


def parse_filter(filter):
    if not filter:
        filter_function = lambda stats: True
    else:
        check_filter(filter)
        # filter_function = lambda stats: stats['max'] > 0.05  # and stats['area'] > 5 and stats['volume'] > 1
        filter = filter.replace('area', 'stats["area"]')
        filter = filter.replace('maxdepth', 'stats["max"]')
        filter = filter.replace('volume', 'stats["volume"]')
        filter = 'lambda stats: {}'.format(filter)
        filter_function = eval(filter)
    return filter_function
