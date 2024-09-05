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

class change_type(Command):
    """
    'change_type' command.
    
    Parameters
    ----------
        zone_list : List
            'zone_list' child.
        new_type : str
            'new_type' child.
    
    """

    fluent_name = "change-type"

    argument_names = \
        ['zone_list', 'new_type']

    _child_classes = dict(
        zone_list=zone_list_cls,
        new_type=new_type_cls,
    )

    return_type = "<object object at 0x7f570357ddb0>"
