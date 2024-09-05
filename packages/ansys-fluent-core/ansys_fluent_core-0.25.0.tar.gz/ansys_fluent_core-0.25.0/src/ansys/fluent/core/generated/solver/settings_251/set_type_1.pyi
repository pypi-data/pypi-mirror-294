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

from .volume_names import volume_names as volume_names_cls
from .type_5 import type as type_cls

class set_type(Command):
    fluent_name = ...
    argument_names = ...
    volume_names: volume_names_cls = ...
    type: type_cls = ...
