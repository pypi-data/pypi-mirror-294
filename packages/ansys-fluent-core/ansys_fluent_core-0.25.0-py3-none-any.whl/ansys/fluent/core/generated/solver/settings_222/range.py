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

from .option import option as option_cls
from .auto_range import auto_range as auto_range_cls
from .clip_to_range_1 import clip_to_range as clip_to_range_cls

class range(Group):
    """
    'range' child.
    """

    fluent_name = "range"

    child_names = \
        ['option', 'auto_range', 'clip_to_range']

    _child_classes = dict(
        option=option_cls,
        auto_range=auto_range_cls,
        clip_to_range=clip_to_range_cls,
    )

    return_type = "<object object at 0x7f57023d3d10>"
