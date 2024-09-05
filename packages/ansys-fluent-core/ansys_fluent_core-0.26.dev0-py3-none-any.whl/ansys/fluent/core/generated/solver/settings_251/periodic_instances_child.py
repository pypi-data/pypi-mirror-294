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

from .name_2 import name as name_cls
from .periodic_type import periodic_type as periodic_type_cls
from .surfaces_13 import surfaces as surfaces_cls
from .translation_1 import translation as translation_cls
from .axis_origin_4 import axis_origin as axis_origin_cls
from .axis_direction_4 import axis_direction as axis_direction_cls
from .angle_3 import angle as angle_cls
from .repeats import repeats as repeats_cls
from .repeats_in_360_degrees import repeats_in_360_degrees as repeats_in_360_degrees_cls

class periodic_instances_child(Group):
    """
    'child_object_type' of periodic_instances.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'periodic_type', 'surfaces', 'translation', 'axis_origin',
         'axis_direction', 'angle', 'repeats', 'repeats_in_360_degrees']

    _child_classes = dict(
        name=name_cls,
        periodic_type=periodic_type_cls,
        surfaces=surfaces_cls,
        translation=translation_cls,
        axis_origin=axis_origin_cls,
        axis_direction=axis_direction_cls,
        angle=angle_cls,
        repeats=repeats_cls,
        repeats_in_360_degrees=repeats_in_360_degrees_cls,
    )

