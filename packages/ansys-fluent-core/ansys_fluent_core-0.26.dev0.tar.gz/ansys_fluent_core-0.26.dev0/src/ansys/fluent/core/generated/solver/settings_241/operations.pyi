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

from .coarsen import coarsen as coarsen_cls
from .refine import refine as refine_cls
from .swap import swap as swap_cls
from .move import move as move_cls

class operations(Group):
    fluent_name = ...
    child_names = ...
    coarsen: coarsen_cls = ...
    refine: refine_cls = ...
    swap: swap_cls = ...
    move: move_cls = ...
    return_type = ...
