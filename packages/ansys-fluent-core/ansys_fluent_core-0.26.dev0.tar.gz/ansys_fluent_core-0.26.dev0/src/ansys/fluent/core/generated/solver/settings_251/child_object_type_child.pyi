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

from .option_2 import option as option_cls
from .constant import constant as constant_cls
from .user_defined import user_defined as user_defined_cls

class child_object_type_child(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    constant: constant_cls = ...
    user_defined: user_defined_cls = ...
