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

from .read_data import read_data as read_data_cls
from .write_data import write_data as write_data_cls

class interpolate(Group):
    fluent_name = ...
    command_names = ...

    def read_data(self, filename: str, cell_zones: List[str]):
        """
        Read and interpolate data.
        
        Parameters
        ----------
            filename : str
                Enter filename for interpolation.
            cell_zones : List
                List of cell zones to import.
        
        """

    def write_data(self, filename_1: str, cell_zones: List[str], fields: List[str], binary_format: bool):
        """
        Write data for interpolation.
        
        Parameters
        ----------
            filename_1 : str
                Enter filename for interpolation.
            cell_zones : List
                List of cell zones to export.
            fields : List
                Field to interpolate.
            binary_format : bool
                Choose whether or not to export in binary format.
        
        """

