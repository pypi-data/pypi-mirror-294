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


class set_damping_strengths(NamedObject[relaxation_factor_child], CreatableNamedObjectMixinOld[relaxation_factor_child]):
    """
    'set_damping_strengths' child.
    """

    fluent_name = "set-damping-strengths"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of set_damping_strengths.
    """
    return_type = "<object object at 0x7f57023d18c0>"
