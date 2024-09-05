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

from .enabled_12 import enabled as enabled_cls
from .file_name import file_name as file_name_cls

class virtual_connection(Command):
    """
    'virtual_connection' command.
    
    Parameters
    ----------
        enabled : bool
            'enabled' child.
        file_name : str
            'file_name' child.
    
    """

    fluent_name = "virtual-connection"

    argument_names = \
        ['enabled', 'file_name']

    _child_classes = dict(
        enabled=enabled_cls,
        file_name=file_name_cls,
    )

    return_type = "<object object at 0x7f5ce12d7760>"
