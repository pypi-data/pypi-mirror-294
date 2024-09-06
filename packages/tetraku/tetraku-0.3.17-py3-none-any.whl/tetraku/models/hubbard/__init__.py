#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021-2024 Hao Zhang<zh970205@mail.ustc.edu.cn>
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
import tetragono as tet


def abstract_state(L1, L2, T, t, U):
    """
    Create Hubbard model state.

    Parameters
    ----------
    L1, L2 : int
        The lattice size.
    T : int
        The half particle number.
    t, U : float
        Hubbard model parameters.
    """
    state = tet.AbstractState(TAT.FermiU1.D.Tensor, L1, L2)
    state.total_symmetry = T
    state.physics_edges[...] = [(0, 1), (1, 2), (2, 1)]
    NN = tet.common_tensor.Fermi_Hubbard.NN.to(float)
    CSCS = tet.common_tensor.Fermi_Hubbard.CSCS.to(float)
    state.hamiltonians["vertical_bond"] = -t * CSCS
    state.hamiltonians["horizontal_bond"] = -t * CSCS
    state.hamiltonians["single_site"] = U * NN
    return state


def abstract_lattice(L1, L2, D, T, t, U):
    """
    Create Hubbard model lattice.

    Parameters
    ----------
    L1, L2 : int
        The lattice size.
    D : int
        The cut dimension.
    T : int
        The half particle number.
    t, U : float
        Hubbard model parameters.
    """
    state = tet.AbstractLattice(abstract_state(L1, L2, T, t, U))
    tt = T / state.L1
    for l1 in range(state.L1 - 1):
        Q = int(T * (state.L1 - l1 - 1) / state.L1)
        state.virtual_bond[l1, 0, "D"] = [(Q - 1, D), (Q, D), (Q + 1, D)]
    for l1 in range(state.L1 - 1):
        for l2 in range(1, state.L2):
            state.virtual_bond[l1, l2, "D"] = [(0, D)]
    for l1 in range(state.L1):
        for l2 in range(state.L2 - 1):
            Q = int(tt * (state.L2 - l2 - 1) / state.L2)
            state.virtual_bond[l1, l2, "R"] = [(Q - 1, D), (Q, D), (Q + 1, D)]

    return state
