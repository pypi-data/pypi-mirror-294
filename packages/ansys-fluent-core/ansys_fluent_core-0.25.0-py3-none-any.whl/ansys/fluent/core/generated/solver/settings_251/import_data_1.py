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

from .memory_id import memory_id as memory_id_cls
from .file_name_29 import file_name as file_name_cls
from .ok_to_discard_data import ok_to_discard_data as ok_to_discard_data_cls

class import_data(Command):
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

    fluent_name = "import-data"

    argument_names = \
        ['memory_id', 'file_name', 'ok_to_discard_data']

    _child_classes = dict(
        memory_id=memory_id_cls,
        file_name=file_name_cls,
        ok_to_discard_data=ok_to_discard_data_cls,
    )

