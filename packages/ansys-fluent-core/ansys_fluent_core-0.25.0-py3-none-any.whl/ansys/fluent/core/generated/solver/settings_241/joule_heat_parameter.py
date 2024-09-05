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
from .value_2 import value as value_cls

class joule_heat_parameter(Group):
    """
    'joule_heat_parameter' child.
    """

    fluent_name = "joule-heat-parameter"

    child_names = \
        ['enabled', 'value']

    _child_classes = dict(
        enabled=enabled_cls,
        value=value_cls,
    )

    return_type = "<object object at 0x7f5d0875d3c0>"
