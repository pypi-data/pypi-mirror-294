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

from .memory_id import memory_id as memory_id_cls
from .file_name_29 import file_name as file_name_cls
from .ok_to_discard_data import ok_to_discard_data as ok_to_discard_data_cls

class import_data(Command):
    fluent_name = ...
    argument_names = ...
    memory_id: memory_id_cls = ...
    file_name: file_name_cls = ...
    ok_to_discard_data: ok_to_discard_data_cls = ...
