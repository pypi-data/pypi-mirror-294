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

from .print_level import print_level as print_level_cls

class mesh_info(Command):
    """
    'mesh_info' command.
    
    Parameters
    ----------
        print_level : int
            Print zone information size.
    
    """

    fluent_name = "mesh-info"

    argument_names = \
        ['print_level']

    _child_classes = dict(
        print_level=print_level_cls,
    )

    return_type = "<object object at 0x7f115d64f7b0>"
