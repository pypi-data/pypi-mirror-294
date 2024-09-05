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

from .option_1 import option as option_cls
from .x_axis_direction import x_axis_direction as x_axis_direction_cls
from .x_axis_function_2 import x_axis_function as x_axis_function_cls

class x_axis_data(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    x_axis_direction: x_axis_direction_cls = ...
    x_axis_function: x_axis_function_cls = ...
