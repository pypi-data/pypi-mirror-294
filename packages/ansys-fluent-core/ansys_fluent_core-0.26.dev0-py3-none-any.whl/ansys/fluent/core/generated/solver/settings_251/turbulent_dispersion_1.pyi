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

from typing import Union, List, Tuple

from .turbulent_dispersion_trans_vof import turbulent_dispersion_trans_vof as turbulent_dispersion_trans_vof_cls
from .turbulent_dispersion_limit_vof import turbulent_dispersion_limit_vof as turbulent_dispersion_limit_vof_cls

class turbulent_dispersion(Group):
    fluent_name = ...
    child_names = ...
    turbulent_dispersion_trans_vof: turbulent_dispersion_trans_vof_cls = ...
    turbulent_dispersion_limit_vof: turbulent_dispersion_limit_vof_cls = ...
