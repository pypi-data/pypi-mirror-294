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

from .relative_tolerance_3 import relative_tolerance as relative_tolerance_cls
from .verbosity_11 import verbosity as verbosity_cls
from .local_smoothing import local_smoothing as local_smoothing_cls
from .smooth_from_ref import smooth_from_ref as smooth_from_ref_cls
from .number_local_layers import number_local_layers as number_local_layers_cls
from .smooth_bl_with_adj import smooth_bl_with_adj as smooth_bl_with_adj_cls

class radial_settings(Group):
    fluent_name = ...
    child_names = ...
    relative_tolerance: relative_tolerance_cls = ...
    verbosity: verbosity_cls = ...
    local_smoothing: local_smoothing_cls = ...
    smooth_from_ref: smooth_from_ref_cls = ...
    number_local_layers: number_local_layers_cls = ...
    smooth_bl_with_adj: smooth_bl_with_adj_cls = ...
