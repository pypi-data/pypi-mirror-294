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

from .fuel import fuel as fuel_cls
from .oxidizer import oxidizer as oxidizer_cls

class species_boundary_child(Group):
    fluent_name = ...
    child_names = ...
    fuel: fuel_cls = ...
    oxidizer: oxidizer_cls = ...
