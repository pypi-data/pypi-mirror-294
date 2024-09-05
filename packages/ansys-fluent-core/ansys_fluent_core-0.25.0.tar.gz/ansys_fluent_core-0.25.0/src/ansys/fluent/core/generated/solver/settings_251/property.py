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

from .nonadianatic_laminar_flame_speed import nonadianatic_laminar_flame_speed as nonadianatic_laminar_flame_speed_cls
from .strained_flame_speed import strained_flame_speed as strained_flame_speed_cls
from .number_heat_loss_points import number_heat_loss_points as number_heat_loss_points_cls
from .recalculate_property import recalculate_property as recalculate_property_cls
from .calculate_strain import calculate_strain as calculate_strain_cls
from .recompute_strain import recompute_strain as recompute_strain_cls

class property(Group):
    """
    PDF Properties Options.
    """

    fluent_name = "property"

    child_names = \
        ['nonadianatic_laminar_flame_speed', 'strained_flame_speed',
         'number_heat_loss_points']

    command_names = \
        ['recalculate_property', 'calculate_strain', 'recompute_strain']

    _child_classes = dict(
        nonadianatic_laminar_flame_speed=nonadianatic_laminar_flame_speed_cls,
        strained_flame_speed=strained_flame_speed_cls,
        number_heat_loss_points=number_heat_loss_points_cls,
        recalculate_property=recalculate_property_cls,
        calculate_strain=calculate_strain_cls,
        recompute_strain=recompute_strain_cls,
    )

