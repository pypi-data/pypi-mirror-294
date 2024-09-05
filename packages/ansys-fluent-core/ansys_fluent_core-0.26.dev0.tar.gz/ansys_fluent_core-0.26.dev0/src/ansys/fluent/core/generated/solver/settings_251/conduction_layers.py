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
from .resize import resize as resize_cls
from .conduction_layers_child import conduction_layers_child


class conduction_layers(ListObject[conduction_layers_child]):
    """
    List of Conduction Layers.
    """

    fluent_name = "conduction-layers"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: conduction_layers_child = conduction_layers_child
    """
    child_object_type of conduction_layers.
    """
