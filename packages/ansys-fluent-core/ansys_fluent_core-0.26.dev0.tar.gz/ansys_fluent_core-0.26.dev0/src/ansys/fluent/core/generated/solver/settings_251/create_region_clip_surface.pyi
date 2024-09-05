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

from .surface_name import surface_name as surface_name_cls
from .type_14 import type as type_cls
from .inclusion import inclusion as inclusion_cls
from .input_coordinates import input_coordinates as input_coordinates_cls
from .surfaces_21 import surfaces as surfaces_cls

class create_region_clip_surface(Command):
    fluent_name = ...
    argument_names = ...
    surface_name: surface_name_cls = ...
    type: type_cls = ...
    inclusion: inclusion_cls = ...
    input_coordinates: input_coordinates_cls = ...
    surfaces: surfaces_cls = ...
