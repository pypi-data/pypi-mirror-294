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

from .activate_flow_boundary_coupling_model import activate_flow_boundary_coupling_model as activate_flow_boundary_coupling_model_cls
from .specify_zones_to_activate import specify_zones_to_activate as specify_zones_to_activate_cls
from .specify_zones_to_deactivate import specify_zones_to_deactivate as specify_zones_to_deactivate_cls

class flow_boundary_coupling(Group):
    fluent_name = ...
    child_names = ...
    activate_flow_boundary_coupling_model: activate_flow_boundary_coupling_model_cls = ...
    specify_zones_to_activate: specify_zones_to_activate_cls = ...
    specify_zones_to_deactivate: specify_zones_to_deactivate_cls = ...
