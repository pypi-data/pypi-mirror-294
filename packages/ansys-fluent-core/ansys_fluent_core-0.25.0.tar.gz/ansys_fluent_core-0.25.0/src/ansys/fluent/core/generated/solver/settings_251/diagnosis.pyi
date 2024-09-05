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

from .print_residuals_by_zone import print_residuals_by_zone as print_residuals_by_zone_cls
from .print_residuals_by_distribution import print_residuals_by_distribution as print_residuals_by_distribution_cls
from .retain_cell_residuals import retain_cell_residuals as retain_cell_residuals_cls

class diagnosis(Group):
    fluent_name = ...
    child_names = ...
    print_residuals_by_zone: print_residuals_by_zone_cls = ...
    print_residuals_by_distribution: print_residuals_by_distribution_cls = ...
    retain_cell_residuals: retain_cell_residuals_cls = ...
