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

from .child_object_type_child import child_object_type_child


class direction_vector_components(ListObject[child_object_type_child]):
    """
    'direction_vector_components' child.
    """

    fluent_name = "direction-vector-components"

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of direction_vector_components.
    """
    return_type = "<object object at 0x7f570323a8c0>"
