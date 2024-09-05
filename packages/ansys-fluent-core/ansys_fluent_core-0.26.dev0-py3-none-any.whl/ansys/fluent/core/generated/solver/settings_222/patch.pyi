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

from .vof_smooth_options import vof_smooth_options as vof_smooth_options_cls

class patch(Group):
    fluent_name = ...
    child_names = ...
    vof_smooth_options: vof_smooth_options_cls = ...
    return_type = ...
