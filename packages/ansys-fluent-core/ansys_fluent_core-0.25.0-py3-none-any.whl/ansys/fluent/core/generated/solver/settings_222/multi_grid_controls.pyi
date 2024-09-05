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

from .multi_grid_controls_child import multi_grid_controls_child


class multi_grid_controls(NamedObject[multi_grid_controls_child], CreatableNamedObjectMixinOld[multi_grid_controls_child]):
    fluent_name = ...
    child_object_type: multi_grid_controls_child = ...
    return_type = ...
