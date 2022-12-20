#!/usr/bin/python

##
# Electrode names for Phoenix and Peregrine
_raw_electrode_names_px = ["GND", "RF"]
_raw_electrode_index_px = {"GND": 0, "RF": 1}
for i in range(10):
    name = f"L{i}"
    _raw_electrode_index_px[name] = len(_raw_electrode_names_px)
    _raw_electrode_names_px.append(name)
for i in range(2):
    name = f"O{i}"
    _raw_electrode_index_px[name] = len(_raw_electrode_names_px)
    _raw_electrode_names_px.append(name)
for i in range(66):
    name = f"Q{i}"
    _raw_electrode_index_px[name] = len(_raw_electrode_names_px)
    _raw_electrode_names_px.append(name)
for i in range(12):
    name = f"S{i}"
    _raw_electrode_index_px[name] = len(_raw_electrode_names_px)
    _raw_electrode_names_px.append(name)

##
# Electrode names for HOA
_raw_electrode_names_hoa = ["GND", "RF"]
_raw_electrode_index_hoa = {"GND": 0, "RF": 1}
for i in range(8):
    name = f"G{i + 1}"
    _raw_electrode_index_hoa[name] = len(_raw_electrode_names_hoa)
    _raw_electrode_names_hoa.append(name)
for i in range(16):
    name = f"L{i + 1}"
    _raw_electrode_index_hoa[name] = len(_raw_electrode_names_hoa)
    _raw_electrode_names_hoa.append(name)
for i in range(40):
    name = f"Q{i + 1}"
    _raw_electrode_index_hoa[name] = len(_raw_electrode_names_hoa)
    _raw_electrode_names_hoa.append(name)
for i in range(6):
    name = f"T{i + 1}"
    _raw_electrode_index_hoa[name] = len(_raw_electrode_names_hoa)
    _raw_electrode_names_hoa.append(name)
for i in range(24):
    name = f"Y{i + 1}"
    _raw_electrode_index_hoa[name] = len(_raw_electrode_names_hoa)
    _raw_electrode_names_hoa.append(name)

def _raw_electrode_names(trap):
    if trap == "phoenix" or trap == "peregrine":
        return _raw_electrode_names_px
    if trap == "hoa":
        return _raw_electrode_names_hoa
    raise ValueError(f"Unknown trap name {trap}")

def _raw_electrode_index(trap):
    if trap == "phoenix" or trap == "peregrine":
        return _raw_electrode_index_px
    if trap == "hoa":
        return _raw_electrode_index_hoa
    raise ValueError(f"Unknown trap name {trap}")
