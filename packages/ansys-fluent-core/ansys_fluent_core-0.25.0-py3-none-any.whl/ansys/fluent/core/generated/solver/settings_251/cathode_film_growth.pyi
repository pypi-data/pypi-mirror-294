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

from .rate_constant_1 import rate_constant as rate_constant_cls
from .ionic_conductivity_1 import ionic_conductivity as ionic_conductivity_cls
from .molecular_weight_2 import molecular_weight as molecular_weight_cls
from .density_2 import density as density_cls

class cathode_film_growth(Group):
    fluent_name = ...
    child_names = ...
    rate_constant: rate_constant_cls = ...
    ionic_conductivity: ionic_conductivity_cls = ...
    molecular_weight: molecular_weight_cls = ...
    density: density_cls = ...
