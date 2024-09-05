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

from .zone_list import zone_list as zone_list_cls
from .new_type import new_type as new_type_cls

class set_zone_type(Command):
    """
    'set_zone_type' command.
    
    Parameters
    ----------
        zone_list : List
            Enter zone name list.
        new_type : str
            'new_type' child.
    
    """

    fluent_name = "set-zone-type"

    argument_names = \
        ['zone_list', 'new_type']

    _child_classes = dict(
        zone_list=zone_list_cls,
        new_type=new_type_cls,
    )

    return_type = "<object object at 0x7f5d08e48b50>"
