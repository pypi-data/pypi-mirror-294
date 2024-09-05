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

from .surface_tension import surface_tension as surface_tension_cls
from .surface_tension_model import surface_tension_model as surface_tension_model_cls
from .surface_tension_model_type import surface_tension_model_type as surface_tension_model_type_cls
from .wall_adhesion import wall_adhesion as wall_adhesion_cls

class forces(Group):
    fluent_name = ...
    child_names = ...
    surface_tension: surface_tension_cls = ...
    surface_tension_model: surface_tension_model_cls = ...
    surface_tension_model_type: surface_tension_model_type_cls = ...
    wall_adhesion: wall_adhesion_cls = ...
