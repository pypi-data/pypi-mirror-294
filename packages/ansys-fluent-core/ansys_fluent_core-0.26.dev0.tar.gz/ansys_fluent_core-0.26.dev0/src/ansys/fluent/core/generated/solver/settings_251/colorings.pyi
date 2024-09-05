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

from .banded_1 import banded as banded_cls
from .smooth import smooth as smooth_cls

class colorings(Group):
    fluent_name = ...
    child_names = ...
    banded: banded_cls = ...
    smooth: smooth_cls = ...
