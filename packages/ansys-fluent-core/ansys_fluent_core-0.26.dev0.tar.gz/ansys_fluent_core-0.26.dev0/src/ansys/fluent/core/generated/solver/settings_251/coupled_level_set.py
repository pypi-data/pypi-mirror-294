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

from .level_set import level_set as level_set_cls
from .weighting import weighting as weighting_cls

class coupled_level_set(Group):
    """
    Set coupled level set.
    """

    fluent_name = "coupled-level-set"

    child_names = \
        ['level_set', 'weighting']

    _child_classes = dict(
        level_set=level_set_cls,
        weighting=weighting_cls,
    )

