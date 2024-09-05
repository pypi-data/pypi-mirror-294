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
from .translation_rotation_matrix_child import translation_rotation_matrix_child


class translation_rotation_matrix(ListObject[translation_rotation_matrix_child]):
    """
    Data class to hold translation-rotation-matrix in the pack builder.
    """

    fluent_name = "translation-rotation-matrix"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: translation_rotation_matrix_child = translation_rotation_matrix_child
    """
    child_object_type of translation_rotation_matrix.
    """
