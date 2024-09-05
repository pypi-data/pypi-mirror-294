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

from .runge_kutta import runge_kutta as runge_kutta_cls

class fast_transient_settings(Group):
    """
    Enter the fast transient settings menu.
    """

    fluent_name = "fast-transient-settings"

    child_names = \
        ['runge_kutta']

    _child_classes = dict(
        runge_kutta=runge_kutta_cls,
    )

    return_type = "<object object at 0x7f115b7b71e0>"
