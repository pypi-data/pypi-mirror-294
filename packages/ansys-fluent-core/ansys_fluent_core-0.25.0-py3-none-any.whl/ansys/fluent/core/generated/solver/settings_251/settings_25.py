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

from .recirculation_inlet import recirculation_inlet as recirculation_inlet_cls
from .geometry_2 import geometry as geometry_cls
from .phase_53 import phase as phase_cls

class settings(Group):
    """
    Select domain name to define settings on.
    """

    fluent_name = "settings"

    child_names = \
        ['recirculation_inlet', 'geometry', 'phase']

    _child_classes = dict(
        recirculation_inlet=recirculation_inlet_cls,
        geometry=geometry_cls,
        phase=phase_cls,
    )

