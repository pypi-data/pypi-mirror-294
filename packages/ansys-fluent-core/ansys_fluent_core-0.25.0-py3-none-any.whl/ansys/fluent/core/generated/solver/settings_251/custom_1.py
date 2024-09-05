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

from .uniform_1 import uniform as uniform_cls
from .timestep_list import timestep_list as timestep_list_cls

class custom(Group):
    """
    Select timesteps uniformly or through timestep list.
    """

    fluent_name = "custom"

    command_names = \
        ['uniform', 'timestep_list']

    _child_classes = dict(
        uniform=uniform_cls,
        timestep_list=timestep_list_cls,
    )

