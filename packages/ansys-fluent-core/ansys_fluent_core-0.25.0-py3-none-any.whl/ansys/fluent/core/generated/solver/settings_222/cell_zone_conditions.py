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

from .fluid_1 import fluid as fluid_cls
from .solid_1 import solid as solid_cls

class cell_zone_conditions(Group):
    """
    'cell_zone_conditions' child.
    """

    fluent_name = "cell-zone-conditions"

    child_names = \
        ['fluid', 'solid']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
    )

    return_type = "<object object at 0x7f5703476f20>"
