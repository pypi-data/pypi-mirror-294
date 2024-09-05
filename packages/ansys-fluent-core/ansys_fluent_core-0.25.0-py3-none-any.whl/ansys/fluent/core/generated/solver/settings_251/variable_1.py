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

from .size_by_1 import size_by as size_by_cls
from .range_1 import range as range_cls
from .range_options_1 import range_options as range_options_cls

class variable(Group):
    """
    'variable' child.
    """

    fluent_name = "variable"

    child_names = \
        ['size_by', 'range', 'range_options']

    _child_classes = dict(
        size_by=size_by_cls,
        range=range_cls,
        range_options=range_options_cls,
    )

