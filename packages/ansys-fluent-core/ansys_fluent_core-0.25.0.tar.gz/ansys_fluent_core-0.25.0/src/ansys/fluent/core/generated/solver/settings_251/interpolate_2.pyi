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

from .export_data_1 import export_data as export_data_cls
from .import_data_1 import import_data as import_data_cls

class interpolate(Group):
    fluent_name = ...
    command_names = ...

    def export_data(self, field: str, file_name: str):
        """
        Export data for interpolation.
        
        Parameters
        ----------
            field : str
                Field to interpolate.
            file_name : str
                Interpolated data file name.
        
        """

    def import_data(self, memory_id: int, file_name: str, ok_to_discard_data: bool):
        """
        Import data for interpolation.
        
        Parameters
        ----------
            memory_id : int
                User-defined memory id to stored interpolated data.
            file_name : str
                Interpolated data file name.
            ok_to_discard_data : bool
                Current data has not been saved, including solution data and any report files, animation files, etc.
        Confirm you want to discard the data and proceed with initialization.
        
        """

