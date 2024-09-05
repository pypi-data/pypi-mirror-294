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

from .tsv_file_name_1 import tsv_file_name_1 as tsv_file_name_1_cls

class import_(Command):
    fluent_name = ...
    argument_names = ...
    tsv_file_name: tsv_file_name_1_cls = ...
