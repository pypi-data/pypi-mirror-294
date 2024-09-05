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


class pb_dqmom_bc(NamedObject[uds_bc_child], CreatableNamedObjectMixinOld[uds_bc_child]):
    """
    'pb_dqmom_bc' child.
    """

    fluent_name = "pb-dqmom-bc"

    child_object_type: uds_bc_child = uds_bc_child
    """
    child_object_type of pb_dqmom_bc.
    """
    return_type = "<object object at 0x7f570335dcc0>"
