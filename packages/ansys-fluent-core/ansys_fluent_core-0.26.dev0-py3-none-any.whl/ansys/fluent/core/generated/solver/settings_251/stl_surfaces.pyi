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

from .surfaces_19 import surfaces as surfaces_cls
from .file_name_25 import file_name as file_name_cls

class stl_surfaces(Command):
    fluent_name = ...
    argument_names = ...
    surfaces: surfaces_cls = ...
    file_name: file_name_cls = ...
