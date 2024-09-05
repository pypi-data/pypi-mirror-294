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

from .inlet_vent_child import inlet_vent_child


class inlet_vent(NamedObject[inlet_vent_child], _NonCreatableNamedObjectMixin[inlet_vent_child]):
    """
    'inlet_vent' child.
    """

    fluent_name = "inlet-vent"

    child_object_type: inlet_vent_child = inlet_vent_child
    """
    child_object_type of inlet_vent.
    """
    return_type = "<object object at 0x7f115c5226a0>"
