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

from .network_end import network_end as network_end_cls
from .phase_43 import phase as phase_cls

class settings(Group):
    fluent_name = ...
    child_names = ...
    network_end: network_end_cls = ...
    phase: phase_cls = ...
