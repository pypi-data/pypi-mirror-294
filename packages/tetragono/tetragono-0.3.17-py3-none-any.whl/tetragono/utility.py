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

import os
import sys
try:
    import cPickle as pickle
except:
    import pickle
import inspect
import signal
from traceback import format_stack
from datetime import datetime
import importlib
import importlib.util
import importlib.machinery
from mpi4py import MPI
import numpy as np
import TAT

clear_line = "\u001b[2K"

mpi_comm = MPI.COMM_WORLD
mpi_rank = mpi_comm.Get_rank()
mpi_size = mpi_comm.Get_size()


def show(*args, **kwargs):
    if mpi_rank == 0:
        print(clear_line, *args, **kwargs, end="\r")


def showln(*args, **kwargs):
    if mpi_rank == 0:
        print(clear_line, *args, **kwargs)


def allreduce_number(number, *, dtype=np.float64):
    buffer = np.array(number, dtype=dtype)
    mpi_comm.Allreduce(MPI.IN_PLACE, buffer)
    return buffer


def allgather_array(array):
    array = np.ascontiguousarray(array)  # Ensure C order
    result = np.zeros([mpi_size, *array.shape], dtype=array.dtype)
    mpi_comm.Allgather(array, result)
    return result


def allreduce_buffer(buffer):
    mpi_comm.Allreduce(MPI.IN_PLACE, buffer)


def allreduce_iterator_buffer(iterator):
    requests = []
    for tensor in iterator:
        requests.append(mpi_comm.Iallreduce(MPI.IN_PLACE, tensor))
    MPI.Request.Waitall(requests)


def allreduce_lattice_buffer(lattice):
    return allreduce_iterator_buffer(tensor.storage for row in lattice for tensor in row)


def bcast_number(number, *, root=0, dtype=np.float64):
    if mpi_rank != root:
        # In cast number is None
        number = 0
    buffer = np.array(number, dtype=dtype)
    mpi_comm.Bcast(buffer, root=root)
    return buffer


def bcast_buffer(buffer, root=0):
    mpi_comm.Bcast(buffer, root=root)


def bcast_iterator_buffer(iterator, root=0):
    requests = []
    for tensor in iterator:
        requests.append(mpi_comm.Ibcast(tensor, root=root))
    MPI.Request.Waitall(requests)


def bcast_lattice_buffer(lattice, root=0):
    return bcast_iterator_buffer((tensor.storage for row in lattice for tensor in row), root=root)


class SignalHandler():

    __slots__ = ["signal", "sigint_recv", "saved_handler"]

    def __init__(self, handler_signal):
        self.signal = handler_signal
        self.sigint_recv = 0
        self.saved_handler = None

    def __enter__(self):

        def handler(signum, frame):
            print(f"\n process {mpi_rank} receive {self.signal.name}, send again to send {self.signal.name}\u001b[2F")
            if self.sigint_recv == 1:
                self.saved_handler(signum, frame)
            else:
                self.sigint_recv = 1

        self.saved_handler = signal.signal(self.signal, handler)
        return self

    def __call__(self):
        if self.sigint_recv:
            print(f" process {mpi_rank} receive {self.signal.name}")
        result = allreduce_number(self.sigint_recv, dtype=np.int64)
        self.sigint_recv = 0
        return result != 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False
        signal.signal(self.signal, self.saved_handler)


class SeedDiffer:

    __slots__ = ["seed"]

    max_int = 2**31
    random_int = TAT.random.uniform_int(0, max_int - 1)

    def make_seed_diff(self):
        self.seed = (self.random_int() + mpi_rank) % self.max_int
        TAT.random.seed(self.seed)
        # c++ random engine will generate the same first uniform int if the seed is near.
        TAT.random.uniform_real(0, 1)()

    def make_seed_same(self):
        self.seed = allreduce_number(self.random_int() // mpi_size, dtype=np.int64)
        TAT.random.seed(self.seed)

    def __enter__(self):
        self.make_seed_diff()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False
        self.make_seed_same()

    def __init__(self):
        self.make_seed_same()


seed_differ = SeedDiffer()


class RenamingUnpickler(pickle.Unpickler):
    """
    TAT 0.3.15 renames symmetry type names.
    This class helps to convert old name to new name.
    """

    def find_class(self, module, name, first=[True, True]):
        rename_dict = {
            "Z2": "BoseZ2",
            "U1": "BoseU1",
            "Fermi": "FermiU1",
            "Parity": "FermiZ2",
            "FermiFermi": "FermiU1FermiU1"
        }
        for old, new in rename_dict.items():
            if module.startswith(f"TAT.{old}.") or module == f"TAT.{old}":
                module = module.replace(old, new)
                if first[0]:
                    first[0] = False
                    showln("###################### Warning begin ####################")
                    showln("Data format before TAT 0.3.15 detected.")
                    showln("Please update the data format as soon as possible.")
                    showln("Load data and dump again would update the format.")
                    showln("####################### Warning end #####################")
        ambiguous_rename_dict = {
            "FermiZ2": "FermiU1BoseZ2",
            "FermiU1": "FermiU1BoseU1",
        }
        for old, new in rename_dict.items():
            if "PYTAT_OLD_SYMMETRY_NAME" in os.environ:
                if module.startswith(f"TAT.{old}.") or module == f"TAT.{old}":
                    module = module.replace(old, new)
            else:
                if first[1]:
                    first[1] = False
                    showln("###################### Warning begin ####################")
                    showln("Reading data with the ambiguous names for symmetry type when update over TAT 0.3.15.")
                    showln("The default behavior is reading in the new format.")
                    showln("For reading old version data, define environment PYTAT_OLD_SYMMETRY_NAME")
                    showln("####################### Warning end #####################")
        return super().find_class(module, name)


def read_from_file(file_name):
    with open(file_name, "rb") as file:
        return RenamingUnpickler(file).load()


def write_to_file(obj, file_name):
    if mpi_rank == 0:
        head, tail = os.path.split(file_name)
        tmp_file_name = os.path.join(head, f".{tail}.tmp")
        with open(tmp_file_name, "wb") as file:
            pickle.dump(obj, file)
        os.rename(tmp_file_name, file_name)
    mpi_comm.Barrier()


@np.vectorize
def lattice_conjugate(tensor):
    return tensor.conjugate(True)


@np.vectorize
def lattice_dot(tensor_1, tensor_2):
    return tensor_1.contract(tensor_2, {(name, name) for name in tensor_1.names}).storage[0]


def lattice_prod_sum(tensors_1, tensors_2):
    dot = lattice_dot(tensors_1, tensors_2)
    return np.sum(dot)


def lattice_update(tensors_1, tensors_2):
    L1, L2 = tensors_1.shape
    for l1 in range(L1):
        for l2 in range(L2):
            tensors_1[l1, l2] += tensors_2[l1, l2]


@np.vectorize
def lattice_randomize(tensor):
    random_same_shape = tensor.same_shape().rand_(0, 1)
    random_same_shape.storage *= np.sign(tensor.storage)
    return random_same_shape


def import_from_tetpath(full_name):
    names = full_name.split(".")
    length = len(names)
    if "TETPATH" in os.environ:
        path = os.environ["TETPATH"].split(":")
    else:
        path = []
    for i in range(length):
        name = ".".join(names[:i + 1])
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec is None:
            raise ModuleNotFoundError(f"No module named '{name}'")
        path = spec.submodule_search_locations
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return module


def import_from_current_dir(full_name):
    names = full_name.split(".")
    length = len(names)
    path = ["."]
    for i in range(length):
        name = ".".join(names[:i + 1])
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec is None:
            raise ModuleNotFoundError(f"No module named '{name}'")
        path = spec.submodule_search_locations
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return module


def get_imported_function(module_name_or_function, function_name):
    if not isinstance(module_name_or_function, str):
        return module_name_or_function
    # 1. current folder
    try:
        module = import_from_current_dir(module_name_or_function)
        return getattr(module, function_name)
    except ModuleNotFoundError as e:
        if not f"No module named '{module_name_or_function}'".startswith(str(e)[:-1]):
            raise
    # 2. TETPATH
    try:
        module = import_from_tetpath(module_name_or_function)
        return getattr(module, function_name)
    except ModuleNotFoundError as e:
        if not f"No module named '{module_name_or_function}'".startswith(str(e)[:-1]):
            raise
    # 3. tetraku
    try:
        module = importlib.import_module("." + module_name_or_function, "tetraku.models")
        return getattr(module, function_name)
    except ModuleNotFoundError as e:
        if not f"No module named 'tetraku.models.{module_name_or_function}'".startswith(str(e)[:-1]):
            raise
    try:
        module = importlib.import_module("." + module_name_or_function, "tetraku.networks")
        return getattr(module, function_name)
    except ModuleNotFoundError as e:
        if not f"No module named 'tetraku.networks.{module_name_or_function}'".startswith(str(e)[:-1]):
            raise
    # 4. normal import
    try:
        module = importlib.import_module(module_name_or_function)
        return getattr(module, function_name)
    except ModuleNotFoundError as e:
        if not f"No module named '{module_name_or_function}'".startswith(str(e)[:-1]):
            raise
    raise ValueError("Invalid module name")


def send(receiver, value):
    try:
        receiver.send(value)
    except StopIteration:
        pass


def safe_contract(tensor_1, tensor_2, pair, *, contract_all_physics_edges=False):
    new_pair = set()
    if contract_all_physics_edges:
        for name in tensor_1.names:
            if str(name)[0] == "P" and name in tensor_2.names:
                new_pair.add((name, name))
    for name_1, name_2 in pair:
        if name_1 in tensor_1.names and name_2 in tensor_2.names:
            new_pair.add((name_1, name_2))

    return tensor_1.contract(tensor_2, new_pair)


def safe_rename(tensor, name_map):
    new_name_map = {}
    for key, value in name_map.items():
        if key in tensor.names:
            new_name_map[key] = value
    return tensor.edge_rename(new_name_map)


def sigusr1_handler(signum, frame):
    with open("tetragono.backtrace", "a", encoding="utf-8") as file:
        file.write((str(mpi_rank) + " " + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "\n" +
                    "".join(format_stack()[:-1]) + "\n"))


if hasattr(signal, "SIGUSR1"):
    signal.signal(signal.SIGUSR1, sigusr1_handler)


def restrict_wrapper(origin_restrict):
    # parameter may be:
    # 1. only configuration
    # 2. configuration and replacement
    if len(inspect.signature(origin_restrict).parameters) == 1:

        def restrict(configuration, replacement=None):
            if replacement is None:
                return origin_restrict(configuration)
            else:
                configuration = configuration.copy()
                for [l1, l2, orbit], new_site_config in replacement.items():
                    configuration[l1, l2, orbit] = new_site_config
                return origin_restrict(configuration)
    else:
        restrict = origin_restrict
    return restrict


def write_configurations(config, file_name):
    config = np.asarray(config, dtype=np.int64)
    file = MPI.File.Open(mpi_comm, file_name, MPI.MODE_WRONLY | MPI.MODE_CREATE)
    shape = config.shape
    head = np.array([mpi_size, len(shape), *shape], dtype=np.int64)
    if mpi_rank == 0:
        file.Write_at(0, head)
    offset = head.nbytes + mpi_rank * config.nbytes
    file.Write_at(offset, config)
    file.Close()


def read_configurations(file_name):
    file = MPI.File.Open(mpi_comm, file_name, MPI.MODE_RDONLY)
    head1 = np.zeros(2, dtype=np.int64)
    file.Read_at(0, head1)
    size, config_rank = head1
    head2 = np.zeros(config_rank, dtype=np.int64)
    file.Read_at(head1.nbytes, head2)
    config = np.zeros(head2, dtype=np.int64)
    if size < mpi_size:
        with seed_differ:
            choose = TAT.random.uniform_int(0, size - 1)()
    else:
        choose = mpi_rank
    offset = head1.nbytes + head2.nbytes + choose * config.nbytes
    file.Read_at(offset, config)
    file.Close()
    return config


def trace_repeated(tensor, points, trace_repeated_pool={}):
    result = tensor

    uniques = []
    # points[i] == uniques[points_to_uniques[i]]
    points_to_uniques = []
    # uniques[i] == points[uniques_to_points[i]], the minimum of all possible value
    uniques_to_points = []
    for index_in_points, point in enumerate(points):
        if point in uniques:
            # Point Apprear before
            index_in_uniques = uniques.index(point)
            points_to_uniques.append(index_in_uniques)
        else:
            # First time for point
            points_to_uniques.append(len(uniques))
            uniques_to_points.append(index_in_points)
            uniques.append(point)

    key = (id(tensor), tuple(points_to_uniques))
    if key not in trace_repeated_pool:
        # 1. trace all same points
        # 2. rename to same points
        # 3. rename to lower index
        trace_set = set()
        rename_map = {}
        for index_in_uniques, _ in enumerate(uniques):
            # Find all point
            index_of_group = [
                index_in_points for index_in_points, another_index_in_uniques in enumerate(points_to_uniques)
                if another_index_in_uniques == index_in_uniques
            ]
            for former, latter in zip(index_of_group[:-1], index_of_group[1:]):
                trace_set.add((f"I{former}", f"O{latter}"))
            rename_map[f"I{index_of_group[-1]}"] = f"I{index_of_group[0]}"
        result = result.trace(trace_set)
        result = result.edge_rename(rename_map)
        result = result.edge_rename({
            f"{direction}{index_in_points}": f"{direction}{index_in_uniques}"
            for index_in_uniques, index_in_points in enumerate(uniques_to_points) for direction in ["I", "O"]
        })
        # tensor must be refered here, otherwise, id(tensor) may be invalid if tensor destructed.
        trace_repeated_pool[key] = (tensor, result)

    return trace_repeated_pool[key][1], tuple(uniques)


def sort_points(tensor, points, sort_points_pool={}):
    sorted_points = tuple(sorted(points))
    order = tuple(sorted_points.index(point) for point in points)
    key = (id(tensor), order)
    if key not in sort_points_pool:
        sorted_tensor = tensor.edge_rename({
            f"{direction}{index_before}": f"{direction}{index_after}" for index_before, index_after in enumerate(order)
            for direction in ["I", "O"]
        })
        # tensor must be refered here, otherwise, id(tensor) may be invalid if tensor destructed.
        sort_points_pool[key] = (tensor, sorted_tensor)
    return sort_points_pool[key][1], sorted_points
