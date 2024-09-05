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

from .turbulence_chemistry_interaction import turbulence_chemistry_interaction as turbulence_chemistry_interaction_cls
from .flame_speed_model import flame_speed_model as flame_speed_model_cls
from .variance_settings import variance_settings as variance_settings_cls

class premix(Group):
    fluent_name = ...
    child_names = ...
    turbulence_chemistry_interaction: turbulence_chemistry_interaction_cls = ...
    flame_speed_model: flame_speed_model_cls = ...
    variance_settings: variance_settings_cls = ...
