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

from .spatial_discretization_limiter import spatial_discretization_limiter as spatial_discretization_limiter_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    spatial_discretization_limiter: spatial_discretization_limiter_cls = ...
    return_type = ...
