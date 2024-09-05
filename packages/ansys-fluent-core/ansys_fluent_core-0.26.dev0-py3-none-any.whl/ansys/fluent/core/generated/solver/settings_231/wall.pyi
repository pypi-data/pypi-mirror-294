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

from .wall_child import wall_child


class wall(NamedObject[wall_child], _NonCreatableNamedObjectMixin[wall_child]):
    fluent_name = ...
    child_object_type: wall_child = ...
    return_type = ...
