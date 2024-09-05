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

from .recirculation_outlet_child import recirculation_outlet_child


class recirculation_outlet(NamedObject[recirculation_outlet_child], _NonCreatableNamedObjectMixin[recirculation_outlet_child]):
    """
    'recirculation_outlet' child.
    """

    fluent_name = "recirculation-outlet"

    child_object_type: recirculation_outlet_child = recirculation_outlet_child
    """
    child_object_type of recirculation_outlet.
    """
    return_type = "<object object at 0x7f115bc7d880>"
