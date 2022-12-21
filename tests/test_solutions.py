#!/usr/bin/python

from trap_dc import solutions

import numpy as np
import pytest

def test_find_flat():
    x, y = np.meshgrid(np.arange(10), np.arange(12), indexing='ij')
    for x0 in np.linspace(0, 8, 10):
        for y0 in np.linspace(0, 8, 10):
            for scale in np.array([-1, -0.1, 0.1, 1]):
                data = (x - x0)**2 + (y - y0)**2 * scale
                assert solutions.find_flat_point(data) == pytest.approx([x0, y0])

    z, x, y = np.meshgrid(np.arange(1000), np.arange(10), np.arange(12), indexing='ij')
    def x0_z(z):
        z = (z - 500) / 500
        return z * 0.5
    def y0_z(z):
        z = (z - 500) / 500
        return z**3 * 0.3
    for scale in np.array([-1, -0.1, 0.1, 1]):
        data = (x - x0_z(z))**2 + (y - y0_z(z))**2 * scale
        xy0 = solutions.find_all_flat_points(data)
        for zi in range(z.shape[0]):
            assert xy0[0, zi] == pytest.approx(x0_z(zi), abs=2e-3)
            assert xy0[1, zi] == pytest.approx(y0_z(zi), abs=2e-3)
