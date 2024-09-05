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

from .change_type import change_type as change_type_cls
from .velocity_inlet_child import velocity_inlet_child


class velocity_inlet(NamedObject[velocity_inlet_child], CreatableNamedObjectMixinOld[velocity_inlet_child]):
    """
    'velocity_inlet' child.
    """

    fluent_name = "velocity-inlet"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: velocity_inlet_child = velocity_inlet_child
    """
    child_object_type of velocity_inlet.
    """
    return_type = "<object object at 0x7f5702640890>"
