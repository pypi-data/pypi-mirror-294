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

from .uniform_1 import uniform as uniform_cls
from .timestep_list import timestep_list as timestep_list_cls

class custom(Group):
    fluent_name = ...
    command_names = ...

    def uniform(self, begin: int, end: int, increment: int):
        """
        Select begin, end and increment for timestep selection.
        
        Parameters
        ----------
            begin : int
                Select begin-timestep for timestep-selector.
            end : int
                Select end-timestep for timestep-selector.
            increment : int
                Select increment for timestep-selector.
        
        """

    def timestep_list(self, timesteps: List[int]):
        """
        Select a list of timesteps.
        
        Parameters
        ----------
            timesteps : List
                Select a list of timesteps.
        
        """

