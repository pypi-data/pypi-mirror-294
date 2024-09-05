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

from .filename_1 import filename_1 as filename_1_cls
from .cell_zones_2 import cell_zones as cell_zones_cls
from .fields import fields as fields_cls
from .binary_format import binary_format as binary_format_cls

class write_data(Command):
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

    fluent_name = "write-data"

    argument_names = \
        ['filename', 'cell_zones', 'fields', 'binary_format']

    _child_classes = dict(
        filename=filename_1_cls,
        cell_zones=cell_zones_cls,
        fields=fields_cls,
        binary_format=binary_format_cls,
    )

