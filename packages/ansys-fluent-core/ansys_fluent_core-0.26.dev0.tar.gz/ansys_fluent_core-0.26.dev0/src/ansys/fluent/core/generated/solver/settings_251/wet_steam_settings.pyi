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

from .max_liquid_mass_fraction import max_liquid_mass_fraction as max_liquid_mass_fraction_cls
from .virial_equation_of_state import virial_equation_of_state as virial_equation_of_state_cls
from .droplet_growth_rate import droplet_growth_rate as droplet_growth_rate_cls
from .stagnation_conditions import stagnation_conditions as stagnation_conditions_cls

class wet_steam_settings(Group):
    fluent_name = ...
    child_names = ...
    max_liquid_mass_fraction: max_liquid_mass_fraction_cls = ...
    virial_equation_of_state: virial_equation_of_state_cls = ...
    droplet_growth_rate: droplet_growth_rate_cls = ...
    stagnation_conditions: stagnation_conditions_cls = ...
