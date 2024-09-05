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

from .cell_registers_child import cell_registers_child


class cell_registers(NamedObject[cell_registers_child], CreatableNamedObjectMixinOld[cell_registers_child]):
    """
    'cell_registers' child.
    """

    fluent_name = "cell-registers"

    child_object_type: cell_registers_child = cell_registers_child
    """
    child_object_type of cell_registers.
    """
    return_type = "<object object at 0x7f115b6a9650>"
