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

from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls

class write_user_setting(Command):
    """
    Write the contents of the Modified Settings Summary table to a file.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "write-user-setting"

    argument_names = \
        ['file_name', 'overwrite']

    _child_classes = dict(
        file_name=file_name_cls,
        overwrite=overwrite_cls,
    )

    return_type = "<object object at 0x7f115b49c4d0>"
