# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Helper to read part of a bliss-tomo acquisition file

Most of the stuff here should be moved as helper from the project
bliss-tomo or inside an independend parser lib at some point.
"""

from __future__ import annotations

import typing
import h5py


class FlatDisplacement(typing.NamedTuple):
    axis_name: str
    relative_motion: tuple[float, str | None] | None
    absolute_motion: tuple[float, str | None] | None


def read_quantity_else_none(group: h5py.Group, name) -> tuple[float, str | None] | None:
    if name not in group:
        return None
    scalar = group[name][()]
    unit = group[name].attrs.get("units", None)
    return scalar, unit


def read_flat_displacement(flat_scan: h5py.Group) -> list[FlatDisplacement]:
    if "technique/flat/displacement" not in flat_scan:
        return []

    result: list[FlatDisplacement] = []

    if "technique/flat/motor" in flat_scan:
        # blisstomo < 2.6
        motors = flat_scan["technique/flat/motor"].asstr()[()]
        relative_motions = flat_scan["technique/flat/displacement"][()]
        unit = flat_scan["technique/flat/displacement"].attrs.get("units", None)
        for i in range(len(motors)):
            f = FlatDisplacement(
                axis_name=motors[i],
                relative_motion=(relative_motions[i], unit),
                absolute_motion=None,
            )
            result.append(f)
        return []

    # blisstomo >= 2.6
    displacement = flat_scan["technique/flat/displacement"]
    for axis_name, node in displacement.items():
        f = FlatDisplacement(
            axis_name=axis_name,
            relative_motion=read_quantity_else_none(node, "relative_position"),
            absolute_motion=read_quantity_else_none(node, "absolute_position"),
        )
        result.append(f)
    return result
