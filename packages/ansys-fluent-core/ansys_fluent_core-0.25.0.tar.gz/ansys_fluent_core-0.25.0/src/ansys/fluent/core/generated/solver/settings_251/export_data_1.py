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

from .field_11 import field as field_cls
from .file_name_29 import file_name as file_name_cls

class export_data(Command):
    """
    Export data for interpolation.
    
    Parameters
    ----------
        field : str
            Field to interpolate.
        file_name : str
            Interpolated data file name.
    
    """

    fluent_name = "export-data"

    argument_names = \
        ['field', 'file_name']

    _child_classes = dict(
        field=field_cls,
        file_name=file_name_cls,
    )

