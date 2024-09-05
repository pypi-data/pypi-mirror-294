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

from .level_set import level_set as level_set_cls
from .weighting import weighting as weighting_cls

class coupled_level_set(Group):
    fluent_name = ...
    child_names = ...
    level_set: level_set_cls = ...
    weighting: weighting_cls = ...
