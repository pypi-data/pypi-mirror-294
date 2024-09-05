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

from .number_grid_points_flamelet import number_grid_points_flamelet as number_grid_points_flamelet_cls
from .number_grid_points_mixture_fraction_space import number_grid_points_mixture_fraction_space as number_grid_points_mixture_fraction_space_cls
from .number_grid_points_progress_variable import number_grid_points_progress_variable as number_grid_points_progress_variable_cls
from .maximum_number_of_flamelets import maximum_number_of_flamelets as maximum_number_of_flamelets_cls
from .scalar_dissipation_stoichiometric import scalar_dissipation_stoichiometric as scalar_dissipation_stoichiometric_cls
from .minimum_scalar_dissipation import minimum_scalar_dissipation as minimum_scalar_dissipation_cls
from .number_grid_points_enthalpy import number_grid_points_enthalpy as number_grid_points_enthalpy_cls
from .nonadiabatic_flamelet import nonadiabatic_flamelet as nonadiabatic_flamelet_cls
from .fully_premix_flamelet import fully_premix_flamelet as fully_premix_flamelet_cls
from .fully_premix_flamelet_mixture_fraction_value import fully_premix_flamelet_mixture_fraction_value as fully_premix_flamelet_mixture_fraction_value_cls
from .initial_scalar_dissipation import initial_scalar_dissipation as initial_scalar_dissipation_cls
from .scalar_dissipation_multiplier import scalar_dissipation_multiplier as scalar_dissipation_multiplier_cls
from .scalar_dissipation_step import scalar_dissipation_step as scalar_dissipation_step_cls
from .udf_flamelet import udf_flamelet as udf_flamelet_cls
from .option_9 import option as option_cls
from .calc_fla import calc_fla as calc_fla_cls
from .write_flamelet_cmd import write_flamelet_cmd as write_flamelet_cmd_cls

class flamelet_parameters(Group):
    fluent_name = ...
    child_names = ...
    number_grid_points_flamelet: number_grid_points_flamelet_cls = ...
    number_grid_points_mixture_fraction_space: number_grid_points_mixture_fraction_space_cls = ...
    number_grid_points_progress_variable: number_grid_points_progress_variable_cls = ...
    maximum_number_of_flamelets: maximum_number_of_flamelets_cls = ...
    scalar_dissipation_stoichiometric: scalar_dissipation_stoichiometric_cls = ...
    minimum_scalar_dissipation: minimum_scalar_dissipation_cls = ...
    number_grid_points_enthalpy: number_grid_points_enthalpy_cls = ...
    nonadiabatic_flamelet: nonadiabatic_flamelet_cls = ...
    fully_premix_flamelet: fully_premix_flamelet_cls = ...
    fully_premix_flamelet_mixture_fraction_value: fully_premix_flamelet_mixture_fraction_value_cls = ...
    initial_scalar_dissipation: initial_scalar_dissipation_cls = ...
    scalar_dissipation_multiplier: scalar_dissipation_multiplier_cls = ...
    scalar_dissipation_step: scalar_dissipation_step_cls = ...
    udf_flamelet: udf_flamelet_cls = ...
    option: option_cls = ...
    command_names = ...

    def calc_fla(self, ):
        """
        Calculate Flamelets.
        """

    def write_flamelet_cmd(self, write_flamelet_file: str):
        """
        Write a flamelet file.
        
        Parameters
        ----------
            write_flamelet_file : str
                Name Flamelet File.
        
        """

