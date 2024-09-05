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

from .wave_list_shallow_child import wave_list_shallow_child


class wave_list_shallow(ListObject[wave_list_shallow_child]):
    """
    'wave_list_shallow' child.
    """

    fluent_name = "wave-list-shallow"

    child_object_type: wave_list_shallow_child = wave_list_shallow_child
    """
    child_object_type of wave_list_shallow.
    """
    return_type = "<object object at 0x7f115bc7ebf0>"
