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

from typing import Union, List, Tuple

from .nonadianatic_laminar_flame_speed import nonadianatic_laminar_flame_speed as nonadianatic_laminar_flame_speed_cls
from .strained_flame_speed import strained_flame_speed as strained_flame_speed_cls
from .number_heat_loss_points import number_heat_loss_points as number_heat_loss_points_cls
from .recalculate_property import recalculate_property as recalculate_property_cls
from .calculate_strain import calculate_strain as calculate_strain_cls
from .recompute_strain import recompute_strain as recompute_strain_cls

class property(Group):
    fluent_name = ...
    child_names = ...
    nonadianatic_laminar_flame_speed: nonadianatic_laminar_flame_speed_cls = ...
    strained_flame_speed: strained_flame_speed_cls = ...
    number_heat_loss_points: number_heat_loss_points_cls = ...
    command_names = ...

    def recalculate_property(self, ):
        """
        Recalculate Properties.
        """

    def calculate_strain(self, ):
        """
        Calculate Strained Flamelets.
        """

    def recompute_strain(self, ):
        """
        Calculate Strained Flamelets.
        """

