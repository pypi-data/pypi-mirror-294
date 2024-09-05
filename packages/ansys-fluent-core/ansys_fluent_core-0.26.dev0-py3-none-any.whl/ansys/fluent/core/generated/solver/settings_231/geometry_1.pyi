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

from .geometry_child import geometry_child


class geometry(NamedObject[geometry_child], CreatableNamedObjectMixinOld[geometry_child]):
    fluent_name = ...
    child_object_type: geometry_child = ...
    return_type = ...
