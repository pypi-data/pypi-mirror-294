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

from .named_expressions_child import named_expressions_child


class named_expressions(NamedObject[named_expressions_child], CreatableNamedObjectMixinOld[named_expressions_child]):
    """
    'named_expressions' child.
    """

    fluent_name = "named-expressions"

    child_object_type: named_expressions_child = named_expressions_child
    """
    child_object_type of named_expressions.
    """
    return_type = "<object object at 0x7f115b7b6b10>"
