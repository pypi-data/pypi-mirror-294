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

from .custom_1 import custom as custom_cls
from .first import first as first_cls
from .last import last as last_cls
from .all_1 import all as all_cls

class timestep_selector(Group):
    """
    Select timesteps for transient postprocessing.
    """

    fluent_name = "timestep-selector"

    child_names = \
        ['custom']

    command_names = \
        ['first', 'last', 'all']

    _child_classes = dict(
        custom=custom_cls,
        first=first_cls,
        last=last_cls,
        all=all_cls,
    )

