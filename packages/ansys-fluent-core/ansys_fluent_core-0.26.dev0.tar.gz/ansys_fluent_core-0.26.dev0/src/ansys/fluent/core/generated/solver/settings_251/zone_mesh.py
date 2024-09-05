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

from .zone_names_4 import zone_names as zone_names_cls

class zone_mesh(Command):
    """
    Draw the mesh defined by specified face zones.
    
    Parameters
    ----------
        zone_names : List
            Enter zone name list.
    
    """

    fluent_name = "zone-mesh"

    argument_names = \
        ['zone_names']

    _child_classes = dict(
        zone_names=zone_names_cls,
    )

