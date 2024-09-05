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

from .pattern import pattern as pattern_cls
from .weight import weight as weight_cls
from .color import color as color_cls

class lines_child(Group):
    """
    'child_object_type' of lines.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pattern', 'weight', 'color']

    _child_classes = dict(
        pattern=pattern_cls,
        weight=weight_cls,
        color=color_cls,
    )

    return_type = "<object object at 0x7f641d552bb0>"
