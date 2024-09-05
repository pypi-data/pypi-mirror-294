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

from .minimum_val import minimum_val as minimum_val_cls
from .maximum_val import maximum_val as maximum_val_cls
from .division_val import division_val as division_val_cls

class histogram_parameters(Group):
    fluent_name = ...
    child_names = ...
    minimum_val: minimum_val_cls = ...
    maximum_val: maximum_val_cls = ...
    division_val: division_val_cls = ...
    return_type = ...
