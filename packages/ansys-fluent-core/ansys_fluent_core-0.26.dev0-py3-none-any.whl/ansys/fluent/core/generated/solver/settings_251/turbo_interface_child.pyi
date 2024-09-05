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

from .name_5 import name as name_cls
from .adjacent_cell_zone_1 import adjacent_cell_zone_1 as adjacent_cell_zone_1_cls
from .zone1_1 import zone1 as zone1_cls
from .adjacent_cell_zone_2 import adjacent_cell_zone_2 as adjacent_cell_zone_2_cls
from .zone2_1 import zone2 as zone2_cls
from .paired_zones import paired_zones as paired_zones_cls
from .turbo_choice_1 import turbo_choice as turbo_choice_cls
from .turbo_non_overlap_1 import turbo_non_overlap as turbo_non_overlap_cls

class turbo_interface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    adjacent_cell_zone_1: adjacent_cell_zone_1_cls = ...
    zone1: zone1_cls = ...
    adjacent_cell_zone_2: adjacent_cell_zone_2_cls = ...
    zone2: zone2_cls = ...
    paired_zones: paired_zones_cls = ...
    turbo_choice: turbo_choice_cls = ...
    turbo_non_overlap: turbo_non_overlap_cls = ...
