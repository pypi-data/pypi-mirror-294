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

from .list_properties_1 import list_properties as list_properties_cls
from .wave_list_child import wave_list_child


class wave_list(ListObject[wave_list_child]):
    """
    'wave_list' child.
    """

    fluent_name = "wave-list"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: wave_list_child = wave_list_child
    """
    child_object_type of wave_list.
    """
    return_type = "<object object at 0x7f641db52f90>"
