#!/usr/bin/python

import os
import os.path
import sys

import h5py
import json
import numpy as np

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_path = os.path.join(root_path, "data")
sys.path.append(root_path)

from trap_dc import solutions, potentials

centers = solutions.CenterTracker(trap="phoenix")
short_map = solutions.load_short_map(
    os.path.join(data_path, "electrode_short_red_202212.csv"))

potential_file = sys.argv[1]
potential = potentials.Potential.import_64(potential_file, aliases=short_map)
fits_cache = solutions.compensate_fitter3(potential)

prefix_dir = os.path.join(data_path, "compensate_red_20221222")
os.makedirs(prefix_dir, exist_ok=True)

def get_rf_center(xpos_um):
    xidx = potential.x_axis_to_index(xpos_um / 1000)
    return (xidx, *centers.get(xidx))

def get_compensate_solution(xpos_um):
    print(f"xpos_um={xpos_um}")
    return solutions.solve_compensate1(fits_cache, get_rf_center(xpos_um),
                                       electrode_min_num=12,
                                       electrode_min_dist=210)

xpos_ums = range(-500, 501)
electrode_names_json = json.dumps(potential.electrode_names)
for xpos_um in xpos_ums:
    eles, voltages = get_compensate_solution(xpos_um)
    with h5py.File(os.path.join(prefix_dir, f"{xpos_um}.h5"), 'w') as fh:
        fh.create_dataset("electrode_names", data=electrode_names_json)
        fh.create_dataset("electrodes", data=eles)
        g = fh.create_group("solutions")
        for name in voltages._fields:
            g.create_dataset(name, data=getattr(voltages, name))
