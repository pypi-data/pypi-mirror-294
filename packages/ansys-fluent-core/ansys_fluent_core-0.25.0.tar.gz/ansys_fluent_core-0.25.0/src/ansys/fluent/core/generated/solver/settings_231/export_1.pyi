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

from .command_name_1 import command_name as command_name_cls
from .tsv_file_name import tsv_file_name as tsv_file_name_cls

class export(Command):
    fluent_name = ...
    argument_names = ...
    command_name: command_name_cls = ...
    tsv_file_name: tsv_file_name_cls = ...
    return_type = ...
