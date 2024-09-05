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

from .lift_child import lift_child


class lift(NamedObject[lift_child], CreatableNamedObjectMixinOld[lift_child]):
    """
    'lift' child.
    """

    fluent_name = "lift"

    child_object_type: lift_child = lift_child
    """
    child_object_type of lift.
    """
    return_type = "<object object at 0x7f57023d2280>"
