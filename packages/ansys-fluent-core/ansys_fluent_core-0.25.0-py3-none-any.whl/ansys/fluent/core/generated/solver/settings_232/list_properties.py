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

class list_properties(Command):
    """
    'list_properties' command.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "list-properties"

    argument_names = \
        ['object_name']

    _child_classes = dict(
        object_name=object_name_cls,
    )

    return_type = "<object object at 0x7f641facd9a0>"
