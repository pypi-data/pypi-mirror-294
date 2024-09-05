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

from .disk_child import disk_child


class disk(NamedObject[disk_child], CreatableNamedObjectMixinOld[disk_child]):
    fluent_name = ...
    child_object_type: disk_child = ...
    return_type = ...
