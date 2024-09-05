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

from .expert_9 import expert as expert_cls
from .interpolate_2 import interpolate as interpolate_cls
from .create_region_clip_surface import create_region_clip_surface as create_region_clip_surface_cls

class utilities(Group):
    """
    Adjoint utilities menu.
    """

    fluent_name = "utilities"

    child_names = \
        ['expert', 'interpolate']

    command_names = \
        ['create_region_clip_surface']

    _child_classes = dict(
        expert=expert_cls,
        interpolate=interpolate_cls,
        create_region_clip_surface=create_region_clip_surface_cls,
    )

