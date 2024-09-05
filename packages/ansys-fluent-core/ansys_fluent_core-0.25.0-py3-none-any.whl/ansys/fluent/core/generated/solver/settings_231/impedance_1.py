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

from .impedance_1_child import impedance_1_child


class impedance_1(ListObject[impedance_1_child]):
    """
    'impedance_1' child.
    """

    fluent_name = "impedance-1"

    child_object_type: impedance_1_child = impedance_1_child
    """
    child_object_type of impedance_1.
    """
    return_type = "<object object at 0x7f115c791b10>"
