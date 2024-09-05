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

from .type_11 import type as type_cls
from .minimum_1 import minimum as minimum_cls
from .maximum_1 import maximum as maximum_cls

class range_options(Group):
    """
    Specify whether you want the range to be Global, Local to the selected zone(s), or Custom.
    """

    fluent_name = "range-options"

    child_names = \
        ['type', 'minimum', 'maximum']

    _child_classes = dict(
        type=type_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
    )

