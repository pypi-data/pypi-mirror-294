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

from .flux_child import flux_child


class flux(NamedObject[flux_child], CreatableNamedObjectMixinOld[flux_child]):
    fluent_name = ...
    child_object_type: flux_child = ...
    return_type = ...
