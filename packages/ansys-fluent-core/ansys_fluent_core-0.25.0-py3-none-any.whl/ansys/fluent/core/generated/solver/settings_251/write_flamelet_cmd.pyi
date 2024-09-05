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

from .write_flamelet_file import write_flamelet_file as write_flamelet_file_cls

class write_flamelet_cmd(Command):
    fluent_name = ...
    argument_names = ...
    write_flamelet_file: write_flamelet_file_cls = ...
