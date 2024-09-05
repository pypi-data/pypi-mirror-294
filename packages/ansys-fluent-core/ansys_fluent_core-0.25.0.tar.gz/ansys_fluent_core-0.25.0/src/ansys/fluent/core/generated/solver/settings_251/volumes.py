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

from .fluid_2 import fluid as fluid_cls
from .solid_3 import solid as solid_cls
from .list_physics import list_physics as list_physics_cls
from .set_type_1 import set_type as set_type_cls

class volumes(Group, _ChildNamedObjectAccessorMixin):
    """
    Set volumes definitions.
    """

    fluent_name = "volumes"

    child_names = \
        ['fluid', 'solid']

    command_names = \
        ['list_physics', 'set_type']

    _child_classes = dict(
        fluid=fluid_cls,
        solid=solid_cls,
        list_physics=list_physics_cls,
        set_type=set_type_cls,
    )

