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

from .mesh_child import mesh_child


class mesh(NamedObject[mesh_child], CreatableNamedObjectMixinOld[mesh_child]):
    fluent_name = ...
    child_object_type: mesh_child = ...
    return_type = ...
