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

from .variance_method import variance_method as variance_method_cls
from .algebraic_variance_constant import algebraic_variance_constant as algebraic_variance_constant_cls

class variance_settings(Group):
    fluent_name = ...
    child_names = ...
    variance_method: variance_method_cls = ...
    algebraic_variance_constant: algebraic_variance_constant_cls = ...
