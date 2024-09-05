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

from .periodic import periodic as periodic_cls
from .geometry_4 import geometry as geometry_cls
from .phase_46 import phase as phase_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    periodic: periodic_cls = ...
    geometry: geometry_cls = ...
    phase: phase_cls = ...
