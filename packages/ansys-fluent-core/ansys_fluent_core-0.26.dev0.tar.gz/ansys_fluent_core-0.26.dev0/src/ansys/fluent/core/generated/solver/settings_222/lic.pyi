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

from .display import display as display_cls
from .lic_child import lic_child


class lic(NamedObject[lic_child], CreatableNamedObjectMixinOld[lic_child]):
    fluent_name = ...
    command_names = ...

    def display(self, object_name: str):
        """
        'display' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
        
        """

    child_object_type: lic_child = ...
    return_type = ...
