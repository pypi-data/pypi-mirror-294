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

from .global_range import global_range as global_range_cls
from .auto_range_1 import auto_range as auto_range_cls
from .clip_to_range import clip_to_range as clip_to_range_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls

class range_options(Group):
    """
    'range_options' child.
    """

    fluent_name = "range-options"

    child_names = \
        ['global_range', 'auto_range', 'clip_to_range', 'minimum', 'maximum']

    _child_classes = dict(
        global_range=global_range_cls,
        auto_range=auto_range_cls,
        clip_to_range=clip_to_range_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
    )

