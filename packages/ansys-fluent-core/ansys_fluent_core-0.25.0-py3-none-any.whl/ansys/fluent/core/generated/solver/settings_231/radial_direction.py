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


class radial_direction(ListObject[child_object_type_child]):
    """
    'radial_direction' child.
    """

    fluent_name = "radial-direction"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of radial_direction.
    """
    return_type = "<object object at 0x7f115c1bf970>"
