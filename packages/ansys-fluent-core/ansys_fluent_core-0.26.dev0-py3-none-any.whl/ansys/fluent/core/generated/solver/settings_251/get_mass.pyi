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

from .cell_zones_10 import cell_zones as cell_zones_cls
from .volumes_1 import volumes as volumes_cls
from .cell_function_2 import cell_function as cell_function_cls
from .current_domain import current_domain as current_domain_cls

class get_mass(Query):
    fluent_name = ...
    argument_names = ...
    cell_zones: cell_zones_cls = ...
    volumes: volumes_cls = ...
    cell_function: cell_function_cls = ...
    current_domain: current_domain_cls = ...
