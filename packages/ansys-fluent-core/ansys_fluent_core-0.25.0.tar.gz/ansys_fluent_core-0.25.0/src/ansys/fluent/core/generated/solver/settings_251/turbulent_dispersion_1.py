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

from .turbulent_dispersion_trans_vof import turbulent_dispersion_trans_vof as turbulent_dispersion_trans_vof_cls
from .turbulent_dispersion_limit_vof import turbulent_dispersion_limit_vof as turbulent_dispersion_limit_vof_cls

class turbulent_dispersion(Group):
    """
    Limiting and transition function controls for turbulent dispersion.
    """

    fluent_name = "turbulent-dispersion"

    child_names = \
        ['turbulent_dispersion_trans_vof', 'turbulent_dispersion_limit_vof']

    _child_classes = dict(
        turbulent_dispersion_trans_vof=turbulent_dispersion_trans_vof_cls,
        turbulent_dispersion_limit_vof=turbulent_dispersion_limit_vof_cls,
    )

