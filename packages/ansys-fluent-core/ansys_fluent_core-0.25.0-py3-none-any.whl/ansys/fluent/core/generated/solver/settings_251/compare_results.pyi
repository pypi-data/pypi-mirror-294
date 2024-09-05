#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    AllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .data_file1 import data_file1 as data_file1_cls
from .data_file2 import data_file2 as data_file2_cls
from .compare import compare as compare_cls

class compare_results(Command):
    fluent_name = ...
    argument_names = ...
    data_file1: data_file1_cls = ...
    data_file2: data_file2_cls = ...
    compare: compare_cls = ...
