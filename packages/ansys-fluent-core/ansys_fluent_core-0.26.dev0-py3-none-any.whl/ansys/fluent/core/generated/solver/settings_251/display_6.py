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

from .surface_mesh_1 import surface_mesh as surface_mesh_cls
from .zone_mesh import zone_mesh as zone_mesh_cls

class display(Group):
    """
    'display' child.
    """

    fluent_name = "display"

    command_names = \
        ['surface_mesh', 'zone_mesh']

    _child_classes = dict(
        surface_mesh=surface_mesh_cls,
        zone_mesh=zone_mesh_cls,
    )

