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

from .angle_1 import angle as angle_cls
from .origin_1 import origin as origin_cls
from .axis_components import axis_components as axis_components_cls

class rotate(Command):
    fluent_name = ...
    argument_names = ...
    angle: angle_cls = ...
    origin: origin_cls = ...
    axis_components: axis_components_cls = ...
