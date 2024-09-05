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

from .filled_1 import filled as filled_cls
from .node_values import node_values as node_values_cls
from .boundary_values import boundary_values as boundary_values_cls
from .contour_lines import contour_lines as contour_lines_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    filled: filled_cls = ...
    node_values: node_values_cls = ...
    boundary_values: boundary_values_cls = ...
    contour_lines: contour_lines_cls = ...
