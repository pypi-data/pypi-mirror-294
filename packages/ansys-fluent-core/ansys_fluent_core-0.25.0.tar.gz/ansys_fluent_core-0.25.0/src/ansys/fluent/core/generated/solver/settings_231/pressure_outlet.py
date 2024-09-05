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

from .pressure_outlet_child import pressure_outlet_child


class pressure_outlet(NamedObject[pressure_outlet_child], _NonCreatableNamedObjectMixin[pressure_outlet_child]):
    """
    'pressure_outlet' child.
    """

    fluent_name = "pressure-outlet"

    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
    return_type = "<object object at 0x7f115bcf4460>"
