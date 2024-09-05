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
from .offsets import offsets as offsets_cls
from .origin import origin as origin_cls
from .axis_1 import axis as axis_cls
from .angles import angles as angles_cls

class copy_cell_zones_by_offsets(Command):
    fluent_name = ...
    argument_names = ...
    cell_zones: cell_zones_cls = ...
    translate: translate_cls = ...
    offsets: offsets_cls = ...
    origin: origin_cls = ...
    axis: axis_cls = ...
    angles: angles_cls = ...
