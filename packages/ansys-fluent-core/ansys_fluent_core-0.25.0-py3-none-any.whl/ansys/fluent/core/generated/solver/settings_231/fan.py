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

from .fan_child import fan_child


class fan(NamedObject[fan_child], _NonCreatableNamedObjectMixin[fan_child]):
    """
    'fan' child.
    """

    fluent_name = "fan"

    child_object_type: fan_child = fan_child
    """
    child_object_type of fan.
    """
    return_type = "<object object at 0x7f115c521a20>"
