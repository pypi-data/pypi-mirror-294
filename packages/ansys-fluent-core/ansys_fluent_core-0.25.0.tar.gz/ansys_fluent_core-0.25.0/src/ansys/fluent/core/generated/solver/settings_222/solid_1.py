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
from .solid_child import solid_child


class solid(NamedObject[solid_child], CreatableNamedObjectMixinOld[solid_child]):
    """
    'solid' child.
    """

    fluent_name = "solid"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
    return_type = "<object object at 0x7f5703475890>"
