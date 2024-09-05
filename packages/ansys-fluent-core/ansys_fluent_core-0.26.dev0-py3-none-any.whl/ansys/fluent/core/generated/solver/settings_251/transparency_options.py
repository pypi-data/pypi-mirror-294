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

from .settings_30 import settings as settings_cls
from .reset_2 import reset as reset_cls
from .invert import invert as invert_cls
from .use_home_tab_range import use_home_tab_range as use_home_tab_range_cls

class transparency_options(Group):
    """
    Provide options for transparncy range(s) for focussing on specific portion of range values(s).
    """

    fluent_name = "transparency-options"

    child_names = \
        ['settings', 'reset', 'invert', 'use_home_tab_range']

    _child_classes = dict(
        settings=settings_cls,
        reset=reset_cls,
        invert=invert_cls,
        use_home_tab_range=use_home_tab_range_cls,
    )

