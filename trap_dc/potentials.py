#!/usr/bin/python

import numpy as np
import struct

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

def _alias_to_names(_aliases, trap):
    """
    Translate an alias map (i.e. to account for electrodes shorting together)
    to a list of electrode names which will be stored in the potential object.

    The keys for the alias map should be the electrodes that are shorted
    to something else and the corresponding values
    should be the ones they got shorted to.
    The order should not make much of a difference except when
    multiple ones are shorted together, in which case the values of the aliases
    should be the same, or when an electrode is effectively shorted to ground,
    in which case the value should be the ground electrode.
    """
    aliases = {}
    raw_electrode_index = _raw_electrode_index(trap)
    for (k, v) in _aliases.items():
        if not isinstance(k, int):
            k = raw_electrode_index[k]
        if not isinstance(v, int):
            v = raw_electrode_index[v]
        aliases[k] = v
    raw_electrode_names = _raw_electrode_names(trap)
    nraw_electrodes = len(raw_electrode_names)
    # This is the mapping between the old electrode index and the new ones.
    id_map = [-1 for i in range(nraw_electrodes)]
    cur_id = 0
    nnew_electrodes = nraw_electrodes - len(aliases)
    electrode_names = [[] for i in range(nnew_electrodes)]
    for i in range(nraw_electrodes):
        if i in aliases:
            continue
        id_map[i] = cur_id
        electrode_names[cur_id].append(raw_electrode_names[i])
        cur_id += 1
    assert nnew_electrodes == cur_id
    for (k, v) in aliases.items():
        # The user should connect directly to the final one
        assert v not in aliases
        new_id = id_map[v]
        assert new_id != -1
        electrode_names[new_id].append(raw_electrode_names[k])
    return electrode_names

class RawPotential:
    @classmethod
    def import_v0(cls, filename):
        self = cls()
        with open(filename, mode="rb") as fh:
            fh.read(4) # discard
            self.electrodes = struct.unpack('<I', fh.read(4))[0]
            self.nx = struct.unpack('<I', fh.read(4))[0]
            self.ny = struct.unpack('<I', fh.read(4))[0]
            self.nz = struct.unpack('<I', fh.read(4))[0]
            vsets = struct.unpack('<I', fh.read(4))[0]
            # Use mm instead of m
            self.stride = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # Use mm instead of m
            self.origin = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # I have no idea what's stored in these
            fh.read(4)
            fh.read(4)
            self.electrodemapping = np.fromfile(fh, np.dtype('<I'), self.electrodes)
            data = np.fromfile(fh, np.dtype('<d'))
            if len(data) != self.electrodes * self.nx * self.ny * self.nz:
                raise ValueError("Did not find the right number of samples")
            self.data = np.reshape(data, (self.electrodes, self.nx, self.ny, self.nz))
        return self

    @classmethod
    def import_v1(cls, filename):
        self = cls()
        with open(filename, mode="rb") as fh:
            fh.read(4) # discard
            self.electrodes = struct.unpack('<I', fh.read(4))[0]
            self.nx = struct.unpack('<I', fh.read(4))[0]
            self.ny = struct.unpack('<I', fh.read(4))[0]
            self.nz = struct.unpack('<I', fh.read(4))[0]
            vsets = struct.unpack('<I', fh.read(4))[0]
            xaxis = (1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0])
            yaxis = (1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0])
            # Use mm instead of m
            self.stride = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # Use mm instead of m
            self.origin = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # I have no idea what's stored in these
            fh.read(4)
            fh.read(4)
            self.electrodemapping = np.fromfile(fh, np.dtype('<I'), self.electrodes)
            data = np.fromfile(fh, np.dtype('<d'))
            if len(data) != self.electrodes * self.nx * self.ny * self.nz:
                raise ValueError("Did not find the right number of samples")
            self.data = np.reshape(data, (self.electrodes, self.nx, self.ny, self.nz))
        return self

    @classmethod
    def import_64(cls, filename):
        self = cls()
        with open(filename, mode="rb") as fh:
            fh.read(8) # discard
            self.electrodes = struct.unpack('<Q', fh.read(8))[0]
            self.nx = struct.unpack('<Q', fh.read(8))[0]
            self.ny = struct.unpack('<Q', fh.read(8))[0]
            self.nz = struct.unpack('<Q', fh.read(8))[0]
            vsets = struct.unpack('<Q', fh.read(8))[0]
            xaxis = (1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0])
            yaxis = (1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0],
                     1000 * struct.unpack('<d', fh.read(8))[0])
            # Use mm instead of m
            self.stride = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # Use mm instead of m
            self.origin = (1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0],
                           1000 * struct.unpack('<d', fh.read(8))[0])
            # I have no idea what's stored in these
            fh.read(8)
            fh.read(8)
            electrodemapping = np.fromfile(fh, np.dtype('<Q'), self.electrodes)
            data = np.fromfile(fh, np.dtype('<d'))
            if len(data) != self.electrodes * self.nx * self.ny * self.nz:
                raise ValueError("Did not find the right number of samples")
            self.data = np.reshape(data, (self.electrodes, self.nx, self.ny, self.nz))
        return self
