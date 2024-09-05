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

from .flamelet_parameters import flamelet_parameters as flamelet_parameters_cls
from .include_equilibrium_flamelet import include_equilibrium_flamelet as include_equilibrium_flamelet_cls
from .pdf_include_equilibrium_flamelet import pdf_include_equilibrium_flamelet as pdf_include_equilibrium_flamelet_cls
from .automatic_refinement import automatic_refinement as automatic_refinement_cls
from .initial_number_grids_flamelet import initial_number_grids_flamelet as initial_number_grids_flamelet_cls
from .maximum_number_grids_flamelet import maximum_number_grids_flamelet as maximum_number_grids_flamelet_cls
from .maximum_change_value_ratio import maximum_change_value_ratio as maximum_change_value_ratio_cls
from .maximum_change_solve_ratio import maximum_change_solve_ratio as maximum_change_solve_ratio_cls
from .refine_based import refine_based as refine_based_cls

class flamelet(Group):
    fluent_name = ...
    child_names = ...
    flamelet_parameters: flamelet_parameters_cls = ...
    include_equilibrium_flamelet: include_equilibrium_flamelet_cls = ...
    pdf_include_equilibrium_flamelet: pdf_include_equilibrium_flamelet_cls = ...
    automatic_refinement: automatic_refinement_cls = ...
    initial_number_grids_flamelet: initial_number_grids_flamelet_cls = ...
    maximum_number_grids_flamelet: maximum_number_grids_flamelet_cls = ...
    maximum_change_value_ratio: maximum_change_value_ratio_cls = ...
    maximum_change_solve_ratio: maximum_change_solve_ratio_cls = ...
    refine_based: refine_based_cls = ...
