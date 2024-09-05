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

from .relaxation_factor_child import relaxation_factor_child


class under_relaxation(NamedObject[relaxation_factor_child], _NonCreatableNamedObjectMixin[relaxation_factor_child]):
    fluent_name = ...
    child_object_type: relaxation_factor_child = ...
    return_type = ...
