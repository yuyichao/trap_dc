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
