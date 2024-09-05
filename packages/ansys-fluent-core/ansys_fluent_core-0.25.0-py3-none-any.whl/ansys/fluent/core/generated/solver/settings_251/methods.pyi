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

from .smoothing_1 import smoothing as smoothing_cls
from .remeshing import remeshing as remeshing_cls
from .layering import layering as layering_cls

class methods(Group):
    fluent_name = ...
    child_names = ...
    smoothing: smoothing_cls = ...
    remeshing: remeshing_cls = ...
    layering: layering_cls = ...
