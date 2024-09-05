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

from .expression_child import expression_child


class expression(NamedObject[expression_child], CreatableNamedObjectMixinOld[expression_child]):
    """
    'expression' child.
    """

    fluent_name = "expression"

    child_object_type: expression_child = expression_child
    """
    child_object_type of expression.
    """
    return_type = "<object object at 0x7f57023d2770>"
