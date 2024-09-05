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

from .option_39 import option as option_cls
from .domain_2 import domain as domain_cls
from .wall_zones_1 import wall_zones as wall_zones_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .momentum_center import momentum_center as momentum_center_cls
from .momentum_axis import momentum_axis as momentum_axis_cls
from .pressure_coordinate import pressure_coordinate as pressure_coordinate_cls
from .coordinate_value import coordinate_value as coordinate_value_cls

class get_forces(Query):
    fluent_name = ...
    argument_names = ...
    option: option_cls = ...
    domain: domain_cls = ...
    wall_zones: wall_zones_cls = ...
    direction_vector: direction_vector_cls = ...
    momentum_center: momentum_center_cls = ...
    momentum_axis: momentum_axis_cls = ...
    pressure_coordinate: pressure_coordinate_cls = ...
    coordinate_value: coordinate_value_cls = ...
