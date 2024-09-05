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

from .absolute_ode_tolerance import absolute_ode_tolerance as absolute_ode_tolerance_cls
from .relative_ode_tolerance import relative_ode_tolerance as relative_ode_tolerance_cls

class integration_options(Group):
    """
    'integration_options' child.
    """

    fluent_name = "integration-options"

    child_names = \
        ['absolute_ode_tolerance', 'relative_ode_tolerance']

    _child_classes = dict(
        absolute_ode_tolerance=absolute_ode_tolerance_cls,
        relative_ode_tolerance=relative_ode_tolerance_cls,
    )

    return_type = "<object object at 0x7f63fefe02e0>"
