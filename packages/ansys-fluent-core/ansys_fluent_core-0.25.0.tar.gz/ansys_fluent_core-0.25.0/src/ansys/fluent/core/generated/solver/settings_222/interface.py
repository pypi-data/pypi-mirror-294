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
from .interface_child import interface_child


class interface(NamedObject[interface_child], CreatableNamedObjectMixinOld[interface_child]):
    """
    'interface' child.
    """

    fluent_name = "interface"

    command_names = \
        ['change_type']

    _child_classes = dict(
        change_type=change_type_cls,
    )

    child_object_type: interface_child = interface_child
    """
    child_object_type of interface.
    """
    return_type = "<object object at 0x7f57030d3470>"
