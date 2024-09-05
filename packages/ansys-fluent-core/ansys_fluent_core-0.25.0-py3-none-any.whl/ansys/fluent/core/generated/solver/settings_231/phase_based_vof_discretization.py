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


class phase_based_vof_discretization(NamedObject[relaxation_factor_child], _NonCreatableNamedObjectMixin[relaxation_factor_child]):
    """
    'phase_based_vof_discretization' child.
    """

    fluent_name = "phase-based-vof-discretization"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of phase_based_vof_discretization.
    """
    return_type = "<object object at 0x7f115b6a83c0>"
