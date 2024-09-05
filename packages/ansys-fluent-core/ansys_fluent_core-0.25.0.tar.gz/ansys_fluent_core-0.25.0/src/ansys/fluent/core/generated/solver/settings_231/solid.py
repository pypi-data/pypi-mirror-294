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

from .solid_child import solid_child


class solid(NamedObject[solid_child], CreatableNamedObjectMixinOld[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
    return_type = "<object object at 0x7f11391aa890>"
