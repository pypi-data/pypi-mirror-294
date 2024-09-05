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

from .change_type import change_type as change_type_cls
from .exhaust_fan_child import exhaust_fan_child


class exhaust_fan(NamedObject[exhaust_fan_child], CreatableNamedObjectMixinOld[exhaust_fan_child]):
    fluent_name = ...
    command_names = ...

    def change_type(self, zone_list: List[str], new_type: str):
        """
        'change_type' command.
        
        Parameters
        ----------
            zone_list : List
                'zone_list' child.
            new_type : str
                'new_type' child.
        
        """

    child_object_type: exhaust_fan_child = ...
    return_type = ...
