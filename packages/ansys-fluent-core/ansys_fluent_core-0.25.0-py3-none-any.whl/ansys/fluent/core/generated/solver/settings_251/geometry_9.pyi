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

from .parameterize_and_explore import parameterize_and_explore as parameterize_and_explore_cls
from .enable_21 import enable as enable_cls

class geometry(Group):
    fluent_name = ...
    child_names = ...
    parameterize_and_explore: parameterize_and_explore_cls = ...
    command_names = ...

    def enable(self, ):
        """
        Enables and loads adjoint module.
        """

