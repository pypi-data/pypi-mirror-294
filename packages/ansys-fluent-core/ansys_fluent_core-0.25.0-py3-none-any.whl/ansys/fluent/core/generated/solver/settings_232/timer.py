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
from .reset_1 import reset as reset_cls

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

    return_type = "<object object at 0x7f641d340770>"
