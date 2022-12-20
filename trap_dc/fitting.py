#!/usr/bin/python

# Copyright (c) 2022 - 2022 Yichao Yu <yyc1992@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not,
# see <http://www.gnu.org/licenses/>.

import math
import numpy as np

# 0-based
def _linear_indices(sizes):
    return range(math.prod(sizes))

def _append_cartisian_indices(res, prefix, sizes):
    size0, *rest_sizes = sizes
    if rest_sizes:
        for i in range(size0):
            _append_cartisian_indices(res, (*prefix, i), rest_sizes)
    else:
        for i in range(size0):
            res.append((*prefix, i))
    return res

# 0-based
# Compared to the julia one, this is eagerly evaluated since I'm way too lazy
# to implement something better, especially without generated functions...
def _cartesian_indices(sizes):
    return _append_cartisian_indices([], (), sizes)

class PolyFitter:
    # center is the origin of the polynomial in index (0-based)
    def __init__(self, orders, sizes=None, center=None):
        orders = np.array(orders, dtype='q')
        self.orders = orders
        if sizes is None:
            sizes = orders + 1
        else:
            sizes = np.array(sizes, dtype='q')
        self.sizes = sizes
        if center is None:
            center = (sizes - 1) / 2
        else:
            center = np.array(center, dtype='d')

        assert (sizes > orders).all()
        nterms = math.prod(orders + 1)
        npoints = math.prod(sizes)

        self.coefficient = np.empty((npoints, nterms))
        pos_lidxs = _linear_indices(sizes)
        pos_cidxs = _cartesian_indices(sizes)
        ord_lidxs = _linear_indices(orders + 1)
        ord_cidxs = _cartesian_indices(orders + 1)
        self.scales = np.empty(nterms)
        scale_max = np.maximum((sizes - 1) / 2, 1.0)
        for iorder in ord_lidxs:
            order = np.array(ord_cidxs[iorder])
            self.scales[iorder] = 1 / math.prod(scale_max**order)

        # Index for position
        for ipos in pos_lidxs:
            # Position of the point, with the origin in the middle of the grid.
            pos = np.array(pos_cidxs[ipos]) - center
            # Index for the polynomial order
            for iorder in ord_lidxs:
                order = np.array(ord_cidxs[iorder])
                self.coefficient[ipos, iorder] = (math.prod(pos**order) *
                                                  self.scales[iorder])
