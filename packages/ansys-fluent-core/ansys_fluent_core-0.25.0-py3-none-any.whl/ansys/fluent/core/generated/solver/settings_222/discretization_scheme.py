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

from .uds_bc_child import uds_bc_child


class discretization_scheme(NamedObject[uds_bc_child], CreatableNamedObjectMixinOld[uds_bc_child]):
    """
    'discretization_scheme' child.
    """

    fluent_name = "discretization-scheme"

    child_object_type: uds_bc_child = uds_bc_child
    """
    child_object_type of discretization_scheme.
    """
    return_type = "<object object at 0x7f57023d1010>"
