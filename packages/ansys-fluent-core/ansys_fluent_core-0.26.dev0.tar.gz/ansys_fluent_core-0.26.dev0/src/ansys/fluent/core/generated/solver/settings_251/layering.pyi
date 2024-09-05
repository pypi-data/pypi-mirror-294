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

from .enabled_41 import enabled as enabled_cls
from .settings_3 import settings as settings_cls

class layering(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    settings: settings_cls = ...
