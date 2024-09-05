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

from .pressure_inlet_child import pressure_inlet_child


class pressure_inlet(NamedObject[pressure_inlet_child], _NonCreatableNamedObjectMixin[pressure_inlet_child]):
    fluent_name = ...
    child_object_type: pressure_inlet_child = ...
    return_type = ...
