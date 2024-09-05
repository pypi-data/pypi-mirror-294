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

from .settings_30 import settings as settings_cls
from .reset_2 import reset as reset_cls
from .invert import invert as invert_cls
from .use_home_tab_range import use_home_tab_range as use_home_tab_range_cls

class transparency_options(Group):
    fluent_name = ...
    child_names = ...
    settings: settings_cls = ...
    reset: reset_cls = ...
    invert: invert_cls = ...
    use_home_tab_range: use_home_tab_range_cls = ...
