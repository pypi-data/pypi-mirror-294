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

from .diagnosis import diagnosis as diagnosis_cls
from .match_fluent_flux_type import match_fluent_flux_type as match_fluent_flux_type_cls

class expert(Group):
    fluent_name = ...
    child_names = ...
    diagnosis: diagnosis_cls = ...
    match_fluent_flux_type: match_fluent_flux_type_cls = ...
