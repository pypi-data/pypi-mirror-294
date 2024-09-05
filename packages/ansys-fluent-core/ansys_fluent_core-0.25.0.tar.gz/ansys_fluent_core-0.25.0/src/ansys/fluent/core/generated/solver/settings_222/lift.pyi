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

from .lift_child import lift_child


class lift(NamedObject[lift_child], CreatableNamedObjectMixinOld[lift_child]):
    fluent_name = ...
    child_object_type: lift_child = ...
    return_type = ...
