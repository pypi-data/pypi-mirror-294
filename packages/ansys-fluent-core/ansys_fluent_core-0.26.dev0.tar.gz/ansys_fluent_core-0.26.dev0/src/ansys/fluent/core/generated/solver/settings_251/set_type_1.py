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

from .volume_names import volume_names as volume_names_cls
from .type_5 import type as type_cls

class set_type(Command):
    """
    Input volume name(s) to change its type.
    
    Parameters
    ----------
        volume_names : List
            Input volume names .
        type : str
            Input volume type.
    
    """

    fluent_name = "set-type"

    argument_names = \
        ['volume_names', 'type']

    _child_classes = dict(
        volume_names=volume_names_cls,
        type=type_cls,
    )

