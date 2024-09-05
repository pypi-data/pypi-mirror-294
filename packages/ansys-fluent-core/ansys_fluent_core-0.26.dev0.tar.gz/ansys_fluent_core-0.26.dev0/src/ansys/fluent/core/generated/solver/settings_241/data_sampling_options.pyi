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

from .data_sets import data_sets as data_sets_cls
from .add_datasets import add_datasets as add_datasets_cls
from .list_datasets import list_datasets as list_datasets_cls

class data_sampling_options(Group):
    fluent_name = ...
    child_names = ...
    data_sets: data_sets_cls = ...
    command_names = ...

    def add_datasets(self, zone_names: List[str], domain: str, quantities: List[str], min: bool, max: bool, mean: bool, rmse: bool, moving_average: bool, average_over: int):
        """
        Add datasets.
        
        Parameters
        ----------
            zone_names : List
                Enter zone name list.
            domain : str
                'domain' child.
            quantities : List
                'quantities' child.
            min : bool
                'min' child.
            max : bool
                'max' child.
            mean : bool
                'mean' child.
            rmse : bool
                'rmse' child.
            moving_average : bool
                'moving_average' child.
            average_over : int
                'average_over' child.
        
        """

    def list_datasets(self, ):
        """
        List dataset.
        """

    return_type = ...
