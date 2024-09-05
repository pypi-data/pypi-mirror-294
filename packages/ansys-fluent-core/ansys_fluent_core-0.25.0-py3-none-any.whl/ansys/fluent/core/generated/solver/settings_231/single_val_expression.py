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

from .single_val_expression_child import single_val_expression_child


class single_val_expression(NamedObject[single_val_expression_child], CreatableNamedObjectMixinOld[single_val_expression_child]):
    """
    'single_val_expression' child.
    """

    fluent_name = "single-val-expression"

    child_object_type: single_val_expression_child = single_val_expression_child
    """
    child_object_type of single_val_expression.
    """
    return_type = "<object object at 0x7f115b6a9140>"
