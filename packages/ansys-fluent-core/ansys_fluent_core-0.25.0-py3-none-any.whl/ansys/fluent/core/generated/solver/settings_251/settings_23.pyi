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

from .radiator import radiator as radiator_cls
from .geometry_2 import geometry as geometry_cls
from .phase_51 import phase as phase_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    radiator: radiator_cls = ...
    geometry: geometry_cls = ...
    phase: phase_cls = ...
