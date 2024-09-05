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


class flow_direction(ListObject[child_object_type_child]):
    """
    'flow_direction' child.
    """

    fluent_name = "flow-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of flow_direction.
    """
    return_type = "<object object at 0x7f115c1beec0>"
