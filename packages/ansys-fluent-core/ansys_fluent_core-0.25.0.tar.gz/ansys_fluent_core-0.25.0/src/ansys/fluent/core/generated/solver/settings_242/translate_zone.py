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

from .zone_names_3 import zone_names as zone_names_cls
from .offset import offset as offset_cls

class translate_zone(Command):
    """
    Translate nodal coordinates of input cell zones.
    
    Parameters
    ----------
        zone_names : List
            Translate specified cell zones.
        offset : List
            'offset' child.
    
    """

    fluent_name = "translate-zone"

    argument_names = \
        ['zone_names', 'offset']

    _child_classes = dict(
        zone_names=zone_names_cls,
        offset=offset_cls,
    )

