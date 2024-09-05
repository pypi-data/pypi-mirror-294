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

from .enabled_54 import enabled as enabled_cls
from .plane import plane as plane_cls

class custom_plane(Group):
    """
    Custom symmetry plane.
    """

    fluent_name = "custom-plane"

    child_names = \
        ['enabled', 'plane']

    _child_classes = dict(
        enabled=enabled_cls,
        plane=plane_cls,
    )

