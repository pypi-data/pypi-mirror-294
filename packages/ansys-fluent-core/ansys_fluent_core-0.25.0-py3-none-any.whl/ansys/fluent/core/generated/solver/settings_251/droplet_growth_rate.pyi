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

from .option_3 import option as option_cls
from .young_alpha import young_alpha as young_alpha_cls
from .young_beta import young_beta as young_beta_cls

class droplet_growth_rate(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    young_alpha: young_alpha_cls = ...
    young_beta: young_beta_cls = ...
