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

from .list import list as list_cls
from .graphics_objects_child import graphics_objects_child


class graphics_objects(NamedObject[graphics_objects_child], CreatableNamedObjectMixinOld[graphics_objects_child]):
    fluent_name = ...
    command_names = ...

    def list(self, ):
        """
        'list' command.
        """

    child_object_type: graphics_objects_child = ...
    return_type = ...
