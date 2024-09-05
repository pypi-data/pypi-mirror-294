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

from .node_values_1 import node_values as node_values_cls

class options(Group):
    """
    'options' child.
    """

    fluent_name = "options"

    child_names = \
        ['node_values']

    _child_classes = dict(
        node_values=node_values_cls,
    )

    return_type = "<object object at 0x7f57022dc1c0>"
