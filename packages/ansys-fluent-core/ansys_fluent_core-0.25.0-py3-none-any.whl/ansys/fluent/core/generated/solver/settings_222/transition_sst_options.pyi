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

from .roughness_correlation import roughness_correlation as roughness_correlation_cls

class transition_sst_options(Group):
    fluent_name = ...
    child_names = ...
    roughness_correlation: roughness_correlation_cls = ...
    return_type = ...
