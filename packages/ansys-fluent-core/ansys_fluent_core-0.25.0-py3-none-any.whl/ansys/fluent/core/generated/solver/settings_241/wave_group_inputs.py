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

from .list_properties import list_properties as list_properties_cls
from .wave_group_inputs_child import wave_group_inputs_child


class wave_group_inputs(ListObject[wave_group_inputs_child]):
    """
    Wave Group Inputs.
    """

    fluent_name = "wave-group-inputs"

    command_names = \
        ['list_properties']

    _child_classes = dict(
        list_properties=list_properties_cls,
    )

    child_object_type: wave_group_inputs_child = wave_group_inputs_child
    """
    child_object_type of wave_group_inputs.
    """
    return_type = "<object object at 0x7f5cfbe206c0>"
