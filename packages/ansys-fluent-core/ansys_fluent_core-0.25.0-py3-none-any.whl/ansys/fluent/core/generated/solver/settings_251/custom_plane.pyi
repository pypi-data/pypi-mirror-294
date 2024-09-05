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

from .enabled_54 import enabled as enabled_cls
from .plane import plane as plane_cls

class custom_plane(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    plane: plane_cls = ...
