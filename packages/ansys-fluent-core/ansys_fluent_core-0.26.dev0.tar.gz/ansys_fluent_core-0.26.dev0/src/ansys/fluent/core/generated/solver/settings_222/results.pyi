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

from .graphics import graphics as graphics_cls
from .surfaces_1 import surfaces as surfaces_cls

class results(Group):
    fluent_name = ...
    child_names = ...
    graphics: graphics_cls = ...
    surfaces: surfaces_cls = ...
    return_type = ...
