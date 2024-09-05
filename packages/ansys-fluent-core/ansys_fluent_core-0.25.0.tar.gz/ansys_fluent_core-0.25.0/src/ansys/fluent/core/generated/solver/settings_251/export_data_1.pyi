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

from .field_11 import field as field_cls
from .file_name_29 import file_name as file_name_cls

class export_data(Command):
    fluent_name = ...
    argument_names = ...
    field: field_cls = ...
    file_name: file_name_cls = ...
