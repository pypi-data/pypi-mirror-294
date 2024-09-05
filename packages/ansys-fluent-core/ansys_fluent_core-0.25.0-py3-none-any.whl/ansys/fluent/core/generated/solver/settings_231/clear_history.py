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

from .object_name import object_name as object_name_cls

class clear_history(Command):
    """
    Clear object history.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "clear-history"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

    return_type = "<object object at 0x7f115b6aa550>"
