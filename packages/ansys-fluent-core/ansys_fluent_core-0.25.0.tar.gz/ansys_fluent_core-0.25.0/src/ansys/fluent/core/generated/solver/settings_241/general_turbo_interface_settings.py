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

from .expert_4 import expert as expert_cls
from .mixing_plane_model_settings import mixing_plane_model_settings as mixing_plane_model_settings_cls

class general_turbo_interface_settings(Group):
    """
    Enter the general turbo interface settings.
    """

    fluent_name = "general-turbo-interface-settings"

    child_names = \
        ['expert', 'mixing_plane_model_settings']

    _child_classes = dict(
        expert=expert_cls,
        mixing_plane_model_settings=mixing_plane_model_settings_cls,
    )

    return_type = "<object object at 0x7f5cfbb867d0>"
