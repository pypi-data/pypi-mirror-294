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

from .continuous_phase import continuous_phase as continuous_phase_cls
from .rough_wall_model_enabled import rough_wall_model_enabled as rough_wall_model_enabled_cls
from .volume_displacement import volume_displacement as volume_displacement_cls

class interaction(Group):
    """
    'interaction' child.
    """

    fluent_name = "interaction"

    child_names = \
        ['continuous_phase', 'rough_wall_model_enabled',
         'volume_displacement']

    _child_classes = dict(
        continuous_phase=continuous_phase_cls,
        rough_wall_model_enabled=rough_wall_model_enabled_cls,
        volume_displacement=volume_displacement_cls,
    )

    return_type = "<object object at 0x7f5ce12d4fd0>"
