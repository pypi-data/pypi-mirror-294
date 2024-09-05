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

from .models import models as models_cls
from .vaporization_pressure import vaporization_pressure as vaporization_pressure_cls
from .non_condensable_gas import non_condensable_gas as non_condensable_gas_cls
from .liquid_surface_tension import liquid_surface_tension as liquid_surface_tension_cls
from .bubble_number_density import bubble_number_density as bubble_number_density_cls
from .hybrid_models import hybrid_models as hybrid_models_cls
from .number_of_phases import number_of_phases as number_of_phases_cls
from .number_of_eulerian_discrete_phases import number_of_eulerian_discrete_phases as number_of_eulerian_discrete_phases_cls
from .vof_sub_models import vof_sub_models as vof_sub_models_cls
from .vof_parameters import vof_parameters as vof_parameters_cls
from .advanced_formulation import advanced_formulation as advanced_formulation_cls
from .phases import phases as phases_cls
from .phase_interaction import phase_interaction as phase_interaction_cls
from .wet_steam_settings import wet_steam_settings as wet_steam_settings_cls

class multiphase(Group):
    """
    Specify multiphase model.
    """

    fluent_name = "multiphase"

    child_names = \
        ['models', 'vaporization_pressure', 'non_condensable_gas',
         'liquid_surface_tension', 'bubble_number_density', 'hybrid_models',
         'number_of_phases', 'number_of_eulerian_discrete_phases',
         'vof_sub_models', 'vof_parameters', 'advanced_formulation', 'phases',
         'phase_interaction', 'wet_steam_settings']

    _child_classes = dict(
        models=models_cls,
        vaporization_pressure=vaporization_pressure_cls,
        non_condensable_gas=non_condensable_gas_cls,
        liquid_surface_tension=liquid_surface_tension_cls,
        bubble_number_density=bubble_number_density_cls,
        hybrid_models=hybrid_models_cls,
        number_of_phases=number_of_phases_cls,
        number_of_eulerian_discrete_phases=number_of_eulerian_discrete_phases_cls,
        vof_sub_models=vof_sub_models_cls,
        vof_parameters=vof_parameters_cls,
        advanced_formulation=advanced_formulation_cls,
        phases=phases_cls,
        phase_interaction=phase_interaction_cls,
        wet_steam_settings=wet_steam_settings_cls,
    )

