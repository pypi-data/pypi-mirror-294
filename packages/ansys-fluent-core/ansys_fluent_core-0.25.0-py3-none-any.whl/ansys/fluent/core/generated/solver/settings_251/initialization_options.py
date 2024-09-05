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

from .initial_pressure import initial_pressure as initial_pressure_cls
from .external_aero import external_aero as external_aero_cls
from .const_velocity import const_velocity as const_velocity_cls

class initialization_options(Group):
    """
    Set Initialization options for the hybrid case.
    """

    fluent_name = "initialization-options"

    child_names = \
        ['initial_pressure', 'external_aero', 'const_velocity']

    _child_classes = dict(
        initial_pressure=initial_pressure_cls,
        external_aero=external_aero_cls,
        const_velocity=const_velocity_cls,
    )

