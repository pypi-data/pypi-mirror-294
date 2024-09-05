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

from .local_dt_dualts_relax import local_dt_dualts_relax as local_dt_dualts_relax_cls
from .global_dt_pseudo_relax import global_dt_pseudo_relax as global_dt_pseudo_relax_cls

class relaxation_factors(Group):
    """
    'relaxation_factors' child.
    """

    fluent_name = "relaxation-factors"

    child_names = \
        ['local_dt_dualts_relax', 'global_dt_pseudo_relax']

    _child_classes = dict(
        local_dt_dualts_relax=local_dt_dualts_relax_cls,
        global_dt_pseudo_relax=global_dt_pseudo_relax_cls,
    )

    return_type = "<object object at 0x7f57023d1e70>"
