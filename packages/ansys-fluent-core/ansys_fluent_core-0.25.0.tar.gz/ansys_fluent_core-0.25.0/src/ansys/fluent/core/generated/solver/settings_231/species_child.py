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


class species_child(NamedObject[relaxation_factor_child], _NonCreatableNamedObjectMixin[relaxation_factor_child]):
    """
    'child_object_type' of species.
    """

    fluent_name = "child-object-type"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of species_child.
    """
    return_type = "<object object at 0x7f115b6aa0d0>"
