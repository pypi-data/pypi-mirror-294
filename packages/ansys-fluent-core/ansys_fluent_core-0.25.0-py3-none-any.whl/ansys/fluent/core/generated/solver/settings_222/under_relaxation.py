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

from .relaxation_factor_child import relaxation_factor_child


class under_relaxation(NamedObject[relaxation_factor_child], CreatableNamedObjectMixinOld[relaxation_factor_child]):
    """
    Enter Under Relaxation Menu.
    """

    fluent_name = "under-relaxation"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of under_relaxation.
    """
    return_type = "<object object at 0x7f57023d0f80>"
