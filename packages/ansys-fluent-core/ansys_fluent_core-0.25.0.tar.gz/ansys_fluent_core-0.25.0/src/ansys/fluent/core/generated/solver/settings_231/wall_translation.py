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

from .axis_direction_child import axis_direction_child


class wall_translation(ListObject[axis_direction_child]):
    """
    'wall_translation' child.
    """

    fluent_name = "wall-translation"

    child_object_type: axis_direction_child = axis_direction_child
    """
    child_object_type of wall_translation.
    """
    return_type = "<object object at 0x7f115ba12f30>"
