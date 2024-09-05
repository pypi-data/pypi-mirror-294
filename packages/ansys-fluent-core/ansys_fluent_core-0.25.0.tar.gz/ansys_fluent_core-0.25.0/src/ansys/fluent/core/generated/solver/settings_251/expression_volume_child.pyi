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

from .name_2 import name as name_cls
from .expression_definition import expression_definition as expression_definition_cls
from .display_4 import display as display_cls

class expression_volume_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    expression_definition: expression_definition_cls = ...
    command_names = ...

    def display(self, ):
        """
        Display a surface.
        """

