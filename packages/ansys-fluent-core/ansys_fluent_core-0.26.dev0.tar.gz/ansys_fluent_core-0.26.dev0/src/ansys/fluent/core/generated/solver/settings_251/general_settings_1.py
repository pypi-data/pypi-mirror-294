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

from .iter_count_1 import iter_count as iter_count_cls
from .explicit_urf import explicit_urf as explicit_urf_cls
from .initialization_options import initialization_options as initialization_options_cls

class general_settings(Group):
    """
    Enter the general settings menu.
    """

    fluent_name = "general-settings"

    child_names = \
        ['iter_count', 'explicit_urf', 'initialization_options']

    _child_classes = dict(
        iter_count=iter_count_cls,
        explicit_urf=explicit_urf_cls,
        initialization_options=initialization_options_cls,
    )

