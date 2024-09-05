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

from .motion_type import motion_type as motion_type_cls
from .constant_velocity import constant_velocity as constant_velocity_cls
from .zone_track import zone_track as zone_track_cls
from .motion_definition import motion_definition as motion_definition_cls

class motion(Group):
    """
    Allows you to give motion properties.
    """

    fluent_name = "motion"

    child_names = \
        ['motion_type', 'constant_velocity', 'zone_track',
         'motion_definition']

    _child_classes = dict(
        motion_type=motion_type_cls,
        constant_velocity=constant_velocity_cls,
        zone_track=zone_track_cls,
        motion_definition=motion_definition_cls,
    )

