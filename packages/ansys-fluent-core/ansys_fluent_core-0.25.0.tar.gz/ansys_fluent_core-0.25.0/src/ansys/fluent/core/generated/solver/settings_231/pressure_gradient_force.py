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

from .option_7 import option as option_cls

class pressure_gradient_force(Group):
    """
    'pressure_gradient_force' child.
    """

    fluent_name = "pressure-gradient-force"

    child_names = \
        ['option']

    _child_classes = dict(
        option=option_cls,
    )

    return_type = "<object object at 0x7f115d64dea0>"
