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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .single_val_expression_child import single_val_expression_child


class single_val_expression(NamedObject[single_val_expression_child], CreatableNamedObjectMixinOld[single_val_expression_child]):
    """
    'single_val_expression' child.
    """

    fluent_name = "single-val-expression"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: single_val_expression_child = single_val_expression_child
    """
    child_object_type of single_val_expression.
    """
    return_type = "<object object at 0x7f641d6624f0>"
