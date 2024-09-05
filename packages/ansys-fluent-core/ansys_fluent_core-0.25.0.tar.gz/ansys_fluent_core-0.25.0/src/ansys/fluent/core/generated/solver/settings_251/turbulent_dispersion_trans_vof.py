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

from .turb_disp_trans_lower_vof import turb_disp_trans_lower_vof as turb_disp_trans_lower_vof_cls
from .turb_disp_trans_upper_vof import turb_disp_trans_upper_vof as turb_disp_trans_upper_vof_cls

class turbulent_dispersion_trans_vof(Group):
    """
    Enter the turbulent dispersion vof transient options menu.
    """

    fluent_name = "turbulent-dispersion-trans-vof"

    child_names = \
        ['turb_disp_trans_lower_vof', 'turb_disp_trans_upper_vof']

    _child_classes = dict(
        turb_disp_trans_lower_vof=turb_disp_trans_lower_vof_cls,
        turb_disp_trans_upper_vof=turb_disp_trans_upper_vof_cls,
    )

