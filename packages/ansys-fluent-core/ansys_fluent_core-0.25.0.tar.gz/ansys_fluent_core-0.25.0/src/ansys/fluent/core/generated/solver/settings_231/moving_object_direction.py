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

from .child_object_type_child_1 import child_object_type_child


class moving_object_direction(ListObject[child_object_type_child]):
    """
    'moving_object_direction' child.
    """

    fluent_name = "moving-object-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of moving_object_direction.
    """
    return_type = "<object object at 0x7f115bc7e170>"
