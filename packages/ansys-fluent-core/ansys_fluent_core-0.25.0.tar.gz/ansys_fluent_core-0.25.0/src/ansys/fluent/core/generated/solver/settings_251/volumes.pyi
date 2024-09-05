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

from .fluid_2 import fluid as fluid_cls
from .solid_3 import solid as solid_cls
from .list_physics import list_physics as list_physics_cls
from .set_type_1 import set_type as set_type_cls

class volumes(Group, _ChildNamedObjectAccessorMixin):
    fluent_name = ...
    child_names = ...
    fluid: fluid_cls = ...
    solid: solid_cls = ...
    command_names = ...

    def list_physics(self, ):
        """
        List volume information.
        """

    def set_type(self, volume_names: List[str], type: str):
        """
        Input volume name(s) to change its type.
        
        Parameters
        ----------
            volume_names : List
                Input volume names .
            type : str
                Input volume type.
        
        """

