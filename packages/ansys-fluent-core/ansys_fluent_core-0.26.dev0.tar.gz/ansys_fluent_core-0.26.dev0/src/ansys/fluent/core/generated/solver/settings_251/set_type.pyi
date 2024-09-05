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

from .boundary_names import boundary_names as boundary_names_cls
from .type_4 import type as type_cls

class set_type(Command):
    fluent_name = ...
    argument_names = ...
    boundary_names: boundary_names_cls = ...
    type: type_cls = ...
