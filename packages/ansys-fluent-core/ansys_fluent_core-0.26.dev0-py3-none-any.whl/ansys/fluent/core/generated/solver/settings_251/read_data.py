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

from .filename import filename as filename_cls
from .cell_zones_1 import cell_zones as cell_zones_cls

class read_data(Command):
    """
    Read and interpolate data.
    
    Parameters
    ----------
        filename : str
            Enter filename for interpolation.
        cell_zones : List
            List of cell zones to import.
    
    """

    fluent_name = "read-data"

    argument_names = \
        ['filename', 'cell_zones']

    _child_classes = dict(
        filename=filename_cls,
        cell_zones=cell_zones_cls,
    )

