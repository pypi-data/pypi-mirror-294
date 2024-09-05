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

from .shell_conduction_child import shell_conduction_child


class shell_conduction(ListObject[shell_conduction_child]):
    fluent_name = ...
    child_object_type: shell_conduction_child = ...
    return_type = ...
