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


class global_dt_pseudo_relax(NamedObject[relaxation_factor_child], _NonCreatableNamedObjectMixin[relaxation_factor_child]):
    """
    'global_dt_pseudo_relax' child.
    """

    fluent_name = "global-dt-pseudo-relax"

    child_object_type: relaxation_factor_child = relaxation_factor_child
    """
    child_object_type of global_dt_pseudo_relax.
    """
    return_type = "<object object at 0x7f115b7b7830>"
