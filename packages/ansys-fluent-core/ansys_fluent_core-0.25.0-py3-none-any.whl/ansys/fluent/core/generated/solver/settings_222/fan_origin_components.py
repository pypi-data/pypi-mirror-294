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

from .axis_direction_component_child import axis_direction_component_child


class fan_origin_components(ListObject[axis_direction_component_child]):
    """
    'fan_origin_components' child.
    """

    fluent_name = "fan-origin-components"

    child_object_type: axis_direction_component_child = axis_direction_component_child
    """
    child_object_type of fan_origin_components.
    """
    return_type = "<object object at 0x7f57031f3f00>"
