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

from .name_1 import name as name_cls

class create(CommandWithPositionalArgs):
    """
    Create an instance of this.
    
    Parameters
    ----------
        name : str
            Set name for an object.
    
    """

    fluent_name = "create"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

    return_type = "string"
