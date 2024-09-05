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

from .turb_disp_limit_lower_vof import turb_disp_limit_lower_vof as turb_disp_limit_lower_vof_cls
from .turb_disp_limit_upper_vof import turb_disp_limit_upper_vof as turb_disp_limit_upper_vof_cls

class turbulent_dispersion_limit_vof_child(Group):
    fluent_name = ...
    child_names = ...
    turb_disp_limit_lower_vof: turb_disp_limit_lower_vof_cls = ...
    turb_disp_limit_upper_vof: turb_disp_limit_upper_vof_cls = ...
