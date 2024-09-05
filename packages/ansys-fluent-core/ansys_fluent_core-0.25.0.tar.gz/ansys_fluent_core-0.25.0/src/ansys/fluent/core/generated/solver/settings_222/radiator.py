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
from .radiator_child import radiator_child


class radiator(NamedObject[radiator_child], CreatableNamedObjectMixinOld[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
    return_type = "<object object at 0x7f5702765b30>"
