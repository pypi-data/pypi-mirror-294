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

from .plane_surface_child import plane_surface_child


class plane_surface(NamedObject[plane_surface_child], CreatableNamedObjectMixinOld[plane_surface_child]):
    fluent_name = ...
    child_object_type: plane_surface_child = ...
    return_type = ...
