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
from .axis_child import axis_child


class degassing(NamedObject[axis_child], CreatableNamedObjectMixinOld[axis_child]):
    """
    'degassing' child.
    """

    fluent_name = "degassing"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: axis_child = axis_child
    """
    child_object_type of degassing.
    """
    return_type = "<object object at 0x7f57034770d0>"
