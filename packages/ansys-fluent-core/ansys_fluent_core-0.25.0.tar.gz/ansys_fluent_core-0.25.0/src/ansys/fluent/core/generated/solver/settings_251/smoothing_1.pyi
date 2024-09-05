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

from .enabled_39 import enabled as enabled_cls
from .method_9 import method as method_cls
from .spring_settings import spring_settings as spring_settings_cls
from .diffusion_settings import diffusion_settings as diffusion_settings_cls
from .linelast_settings import linelast_settings as linelast_settings_cls
from .radial_settings import radial_settings as radial_settings_cls

class smoothing(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    method: method_cls = ...
    spring_settings: spring_settings_cls = ...
    diffusion_settings: diffusion_settings_cls = ...
    linelast_settings: linelast_settings_cls = ...
    radial_settings: radial_settings_cls = ...
