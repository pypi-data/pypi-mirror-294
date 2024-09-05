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

from .periodic import periodic as periodic_cls
from .geometry_4 import geometry as geometry_cls
from .phase_46 import phase as phase_cls

class settings(Group):
    """
    Select domain name to define settings on.
    """

    fluent_name = "settings"

    child_names = \
        ['periodic', 'geometry', 'phase']

    _child_classes = dict(
        periodic=periodic_cls,
        geometry=geometry_cls,
        phase=phase_cls,
    )

