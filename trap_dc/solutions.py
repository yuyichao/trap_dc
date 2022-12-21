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

from . import fitting

import os
import os.path
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

import h5py
import numpy as np
from scipy.optimize import fsolve

def find_flat_point(data, init=None):
    N = data.ndim
    if init is None:
        init = [(s - 1) / 2 for s in data.shape]
    init = np.array(init)
    # 3rd order fit
    fitter = fitting.PolyFitter(tuple(3 for i in range(N)))
    cache = fitting.PolyFitCache(fitter, data)
    def model(x):
        return np.array([cache.gradient(i, x) for i in range(N)])
    return fsolve(model, init)

def find_all_flat_points(all_data, init=None):
    N = all_data.ndim
    npoints = all_data.shape[0]
    all_res = np.empty((N - 1, npoints))
    if init is None:
        init = [(s - 1) / 2 for s in all_data.shape[1:]]
    for i in range(npoints):
        idx_range = (i,) + tuple(slice(None) for i in range(N - 1))
        init = find_flat_point(all_data[idx_range], init=init)
        all_res[:, i] = init
    return all_res

# EURIQA unit:
# Unit such that electric potential that creates 1MHz trapping frequency
# for Yb171 has the form X^2/2,
# and the electric potential between two ions is 1/r.

N_A = 6.02214076e23
m_Yb171 = 170.9363315e-3 / N_A # kg
q_e = 1.60217663e-19 # C
epsilon_0 = 8.8541878128e-12

A = m_Yb171 * (2 * np.pi * 1e6)**2 / q_e
B = q_e / (4 * np.pi * epsilon_0)

V_unit = np.cbrt(A * B**2) # V
l_unit = np.cbrt(B / A) # m

del A
del B

l_unit_um = l_unit * 1e6 # um
V_unit_uV = V_unit * 1e6 # uV

class CenterTracker:
    def __init__(self, trap=None, filename=None):
        if filename is None:
            if trap is None:
                raise ValueError('Must specify either "trap" or "filename"')
            filename = os.path.join(root_path, "data", f"rf_center_{trap}.h5")
        with h5py.File(filename, 'r') as fh:
            self.yz_index = np.array(fh['yz_index'])

    def get(self, xidx):
        # return (y, z)
        nx = self.yz_index.shape[1]
        lb_idx = min(max(int(np.floor(xidx)), 0), nx - 1)
        ub_idx = min(max(int(np.ceil(xidx)), 0), nx - 1)
        y_lb = self.yz_index[0, lb_idx]
        z_lb = self.yz_index[1, lb_idx]
        if lb_idx == ub_idx:
            return y_lb, z_lb
        assert ub_idx == lb_idx + 1
        y_ub = self.yz_index[0, ub_idx]
        z_ub = self.yz_index[1, ub_idx]
        c_ub = xidx - lb_idx
        c_lb = ub_idx - xidx
        return y_lb * c_lb + y_ub * c_ub, z_lb * c_lb + z_ub * c_ub
