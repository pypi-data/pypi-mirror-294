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

from .mg_controls_child import mg_controls_child


class mg_controls(NamedObject[mg_controls_child], _NonCreatableNamedObjectMixin[mg_controls_child]):
    fluent_name = ...
    child_object_type: mg_controls_child = ...
    return_type = ...
