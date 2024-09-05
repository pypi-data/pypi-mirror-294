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

from .filename import filename as filename_cls
from .cell_zones_1 import cell_zones as cell_zones_cls

class read_data(Command):
    fluent_name = ...
    argument_names = ...
    filename: filename_cls = ...
    cell_zones: cell_zones_cls = ...
