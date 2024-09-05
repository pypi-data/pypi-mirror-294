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

from .number_grid_points_progress_variable_1 import number_grid_points_progress_variable as number_grid_points_progress_variable_cls
from .number_grid_points_pdf import number_grid_points_pdf as number_grid_points_pdf_cls
from .number_grid_points_progress_variable_variance import number_grid_points_progress_variable_variance as number_grid_points_progress_variable_variance_cls
from .number_grid_points_mixture_fraction_variance import number_grid_points_mixture_fraction_variance as number_grid_points_mixture_fraction_variance_cls
from .initial_grid_points import initial_grid_points as initial_grid_points_cls
from .maximum_grid_points import maximum_grid_points as maximum_grid_points_cls
from .maximum_change_value_ratio import maximum_change_value_ratio as maximum_change_value_ratio_cls
from .maximum_change_slope_ratio import maximum_change_slope_ratio as maximum_change_slope_ratio_cls
from .maximum_species import maximum_species as maximum_species_cls
from .mean_enthalpy_points import mean_enthalpy_points as mean_enthalpy_points_cls
from .minimum_temperature import minimum_temperature as minimum_temperature_cls
from .automatic_grid_refinement import automatic_grid_refinement as automatic_grid_refinement_cls

class table_parameters(Group):
    fluent_name = ...
    child_names = ...
    number_grid_points_progress_variable: number_grid_points_progress_variable_cls = ...
    number_grid_points_pdf: number_grid_points_pdf_cls = ...
    number_grid_points_progress_variable_variance: number_grid_points_progress_variable_variance_cls = ...
    number_grid_points_mixture_fraction_variance: number_grid_points_mixture_fraction_variance_cls = ...
    initial_grid_points: initial_grid_points_cls = ...
    maximum_grid_points: maximum_grid_points_cls = ...
    maximum_change_value_ratio: maximum_change_value_ratio_cls = ...
    maximum_change_slope_ratio: maximum_change_slope_ratio_cls = ...
    maximum_species: maximum_species_cls = ...
    mean_enthalpy_points: mean_enthalpy_points_cls = ...
    minimum_temperature: minimum_temperature_cls = ...
    automatic_grid_refinement: automatic_grid_refinement_cls = ...
