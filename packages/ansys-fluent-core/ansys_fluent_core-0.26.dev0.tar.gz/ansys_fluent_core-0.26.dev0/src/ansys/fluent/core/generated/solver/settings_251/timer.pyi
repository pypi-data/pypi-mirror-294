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

from .usage import usage as usage_cls
from .reset_5 import reset as reset_cls

class timer(Group):
    fluent_name = ...
    command_names = ...

    def usage(self, ):
        """
        Print solver timer.
        """

    def reset(self, ):
        """
        Reset domain timers.
        """

