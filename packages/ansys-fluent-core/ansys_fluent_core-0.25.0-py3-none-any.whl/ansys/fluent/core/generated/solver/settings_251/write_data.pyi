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

from .filename_1 import filename_1 as filename_1_cls
from .cell_zones_2 import cell_zones as cell_zones_cls
from .fields import fields as fields_cls
from .binary_format import binary_format as binary_format_cls

class write_data(Command):
    fluent_name = ...
    argument_names = ...
    filename: filename_1_cls = ...
    cell_zones: cell_zones_cls = ...
    fields: fields_cls = ...
    binary_format: binary_format_cls = ...
