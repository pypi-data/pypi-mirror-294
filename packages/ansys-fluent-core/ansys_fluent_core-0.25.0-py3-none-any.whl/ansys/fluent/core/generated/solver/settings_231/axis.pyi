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

from .axis_child import axis_child


class axis(NamedObject[axis_child], _NonCreatableNamedObjectMixin[axis_child]):
    fluent_name = ...
    child_object_type: axis_child = ...
    return_type = ...
