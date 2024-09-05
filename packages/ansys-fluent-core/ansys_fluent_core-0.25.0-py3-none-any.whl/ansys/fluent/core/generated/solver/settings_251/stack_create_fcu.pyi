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

from .fcu_name import fcu_name as fcu_name_cls
from .cellzones_2 import cellzones as cellzones_cls

class stack_create_fcu(Command):
    fluent_name = ...
    argument_names = ...
    fcu_name: fcu_name_cls = ...
    cellzones: cellzones_cls = ...
