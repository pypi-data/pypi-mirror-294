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
from .child_object_type_child_2 import child_object_type_child


class terms_child(ListObject[child_object_type_child]):
    """
    'child_object_type' of terms.
    """

    fluent_name = "child-object-type"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: child_object_type_child = child_object_type_child
    """
    child_object_type of terms_child.
    """
