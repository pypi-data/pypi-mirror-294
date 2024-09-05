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

from .color import color as color_cls
from .weight import weight as weight_cls

class major_gridlines(Group):
    fluent_name = ...
    child_names = ...
    color: color_cls = ...
    weight: weight_cls = ...
    return_type = ...
