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

from .custom_1 import custom as custom_cls
from .first import first as first_cls
from .last import last as last_cls
from .all_1 import all as all_cls

class timestep_selector(Group):
    fluent_name = ...
    child_names = ...
    custom: custom_cls = ...
    command_names = ...

    def first(self, ):
        """
        Select first timestep.
        """

    def last(self, ):
        """
        Select last timestep.
        """

    def all(self, ):
        """
        Select all timesteps.
        """

