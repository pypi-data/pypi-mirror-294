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

from .zone_name_6 import zone_name as zone_name_cls
from .abbreviate_types import abbreviate_types as abbreviate_types_cls
from .exclude import exclude as exclude_cls

class rename_by_adjacency(Command):
    """
    Rename zone to adjacent zones.
    
    Parameters
    ----------
        zone_name : List
            Enter zone name list.
        abbreviate_types : bool
            'abbreviate_types' child.
        exclude : bool
            'exclude' child.
    
    """

    fluent_name = "rename-by-adjacency"

    argument_names = \
        ['zone_name', 'abbreviate_types', 'exclude']

    _child_classes = dict(
        zone_name=zone_name_cls,
        abbreviate_types=abbreviate_types_cls,
        exclude=exclude_cls,
    )

    return_type = "<object object at 0x7f5cfbb85760>"
