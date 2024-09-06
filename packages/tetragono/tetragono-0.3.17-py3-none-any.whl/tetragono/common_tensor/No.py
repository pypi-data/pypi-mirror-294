#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2020-2024 Hao Zhang<zh970205@mail.ustc.edu.cn>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import TAT
from .tensor_toolkit import rename_io, kronecker_product

Tensor = TAT.No.Z.Tensor

identity = Tensor(["I0", "O0"], [2, 2]).zero_()
identity[{"I0": 0, "O0": 0}] = 1
identity[{"I0": 1, "O0": 1}] = 1

pauli_x = Tensor(["I0", "O0"], [2, 2]).zero_()
pauli_x[{"I0": 0, "O0": 1}] = 1
pauli_x[{"I0": 1, "O0": 0}] = 1
Sx = pauli_x / 2

pauli_y = Tensor(["I0", "O0"], [2, 2]).zero_()
pauli_y[{"I0": 0, "O0": 1}] = -1j
pauli_y[{"I0": 1, "O0": 0}] = +1j
Sy = pauli_y / 2

pauli_z = Tensor(["I0", "O0"], [2, 2]).zero_()
pauli_z[{"I0": 0, "O0": 0}] = +1
pauli_z[{"I0": 1, "O0": 1}] = -1
Sz = pauli_z / 2

pauli_x_pauli_x = kronecker_product(
    rename_io(pauli_x, [0]),
    rename_io(pauli_x, [1]),
)
pauli_y_pauli_y = kronecker_product(
    rename_io(pauli_y, [0]),
    rename_io(pauli_y, [1]),
)
pauli_z_pauli_z = kronecker_product(
    rename_io(pauli_z, [0]),
    rename_io(pauli_z, [1]),
)
SxSx = pauli_x_pauli_x / 4
SySy = pauli_y_pauli_y / 4
SzSz = pauli_z_pauli_z / 4

SS = SxSx + SySy + SzSz
