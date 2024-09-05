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

from .boundary_names import boundary_names as boundary_names_cls
from .type_4 import type as type_cls

class set_type(Command):
    """
    Input volume name(s) to change its type.
    
    Parameters
    ----------
        boundary_names : List
            Input boundary names .
        type : str
            Input boundary type.
    
    """

    fluent_name = "set-type"

    argument_names = \
        ['boundary_names', 'type']

    _child_classes = dict(
        boundary_names=boundary_names_cls,
        type=type_cls,
    )

