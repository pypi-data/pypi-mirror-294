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

from .enabled_38 import enabled as enabled_cls
from .methods import methods as methods_cls

class dynamic_mesh(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    methods: methods_cls = ...
