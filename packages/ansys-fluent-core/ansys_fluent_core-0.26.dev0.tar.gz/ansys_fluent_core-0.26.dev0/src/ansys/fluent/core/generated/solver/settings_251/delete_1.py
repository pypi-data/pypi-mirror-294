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

from .name_list import name_list as name_list_cls

class delete(CommandWithPositionalArgs):
    """
    Delete selected objects.
    
    Parameters
    ----------
        name_list : List
            Select objects to be deleted.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['name_list']

    _child_classes = dict(
        name_list=name_list_cls,
    )

