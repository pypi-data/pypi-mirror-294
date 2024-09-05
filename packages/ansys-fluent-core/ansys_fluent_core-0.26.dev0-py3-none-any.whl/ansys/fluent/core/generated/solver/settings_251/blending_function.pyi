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

from .option_5 import option as option_cls
from .expression_1 import expression as expression_cls
from .user_defined_2 import user_defined as user_defined_cls

class blending_function(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    expression: expression_cls = ...
    user_defined: user_defined_cls = ...
