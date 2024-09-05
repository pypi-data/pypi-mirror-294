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

from .enable_6 import enable as enable_cls
from .turbulent_approximation import turbulent_approximation as turbulent_approximation_cls

class convective_heat_transfer(Group):
    """
    'convective_heat_transfer' child.
    """

    fluent_name = "convective-heat-transfer"

    child_names = \
        ['enable', 'turbulent_approximation']

    _child_classes = dict(
        enable=enable_cls,
        turbulent_approximation=turbulent_approximation_cls,
    )

    return_type = "<object object at 0x7f63fefe1590>"
