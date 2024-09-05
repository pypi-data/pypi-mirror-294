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

from .enable import enable as enable_cls
from .time_delay import time_delay as time_delay_cls

class particle_reinjector(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    time_delay: time_delay_cls = ...
    return_type = ...
