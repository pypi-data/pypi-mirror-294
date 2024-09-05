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

from .cell_zones_5 import cell_zones as cell_zones_cls
from .translate_1 import translate as translate_cls
from .ncopies import ncopies as ncopies_cls
from .offset_1 import offset as offset_cls
from .origin import origin as origin_cls
from .axis_1 import axis as axis_cls
from .angle import angle as angle_cls

class copy_cell_zones_by_delta(Command):
    fluent_name = ...
    argument_names = ...
    cell_zones: cell_zones_cls = ...
    translate: translate_cls = ...
    ncopies: ncopies_cls = ...
    offset: offset_cls = ...
    origin: origin_cls = ...
    axis: axis_cls = ...
    angle: angle_cls = ...
