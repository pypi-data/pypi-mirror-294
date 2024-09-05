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

from .cell_registers_child import cell_registers_child


class cell_registers(NamedObject[cell_registers_child], CreatableNamedObjectMixinOld[cell_registers_child]):
    fluent_name = ...
    child_object_type: cell_registers_child = ...
    return_type = ...
