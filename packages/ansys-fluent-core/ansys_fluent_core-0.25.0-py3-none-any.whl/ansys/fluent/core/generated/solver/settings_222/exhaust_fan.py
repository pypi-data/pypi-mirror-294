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
from .exhaust_fan_child import exhaust_fan_child


class exhaust_fan(NamedObject[exhaust_fan_child], CreatableNamedObjectMixinOld[exhaust_fan_child]):
    """
    'exhaust_fan' child.
    """

    fluent_name = "exhaust-fan"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: exhaust_fan_child = exhaust_fan_child
    """
    child_object_type of exhaust_fan.
    """
    return_type = "<object object at 0x7f5703477230>"
