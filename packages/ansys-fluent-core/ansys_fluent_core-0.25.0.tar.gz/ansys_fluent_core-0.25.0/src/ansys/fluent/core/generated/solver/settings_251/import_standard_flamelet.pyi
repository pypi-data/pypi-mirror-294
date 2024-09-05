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

from .standard_flamelet_file import standard_flamelet_file as standard_flamelet_file_cls

class import_standard_flamelet(Command):
    fluent_name = ...
    argument_names = ...
    standard_flamelet_file: standard_flamelet_file_cls = ...
