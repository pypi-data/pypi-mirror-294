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

from .usage import usage as usage_cls
from .reset_5 import reset as reset_cls

class timer(Group):
    """
    'timer' child.
    """

    fluent_name = "timer"

    command_names = \
        ['usage', 'reset']

    _child_classes = dict(
        usage=usage_cls,
        reset=reset_cls,
    )

