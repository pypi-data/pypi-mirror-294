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

from .chemistry import chemistry as chemistry_cls
from .boundary import boundary as boundary_cls
from .control import control as control_cls
from .flamelet import flamelet as flamelet_cls
from .table import table as table_cls
from .premix import premix as premix_cls
from .property import property as property_cls

class partially_premixed_model_options(Group):
    fluent_name = ...
    child_names = ...
    chemistry: chemistry_cls = ...
    boundary: boundary_cls = ...
    control: control_cls = ...
    flamelet: flamelet_cls = ...
    table: table_cls = ...
    premix: premix_cls = ...
    property: property_cls = ...
