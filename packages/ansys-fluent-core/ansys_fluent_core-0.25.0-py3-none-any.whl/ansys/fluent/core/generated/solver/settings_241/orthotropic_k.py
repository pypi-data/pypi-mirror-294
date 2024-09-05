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

from .enabled_12 import enabled as enabled_cls
from .value_input import value_input as value_input_cls

class orthotropic_k(Group):
    """
    'orthotropic_k' child.
    """

    fluent_name = "orthotropic-k"

    child_names = \
        ['enabled', 'value_input']

    _child_classes = dict(
        enabled=enabled_cls,
        value_input=value_input_cls,
    )

    return_type = "<object object at 0x7f5d0875d650>"
