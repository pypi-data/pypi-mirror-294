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

from .operating_pressure_1 import operating_pressure as operating_pressure_cls
from .equilibrium_operating_pressure import equilibrium_operating_pressure as equilibrium_operating_pressure_cls

class model_settings(Group):
    """
    Model Settings for Pressure.
    """

    fluent_name = "model-settings"

    child_names = \
        ['operating_pressure', 'equilibrium_operating_pressure']

    _child_classes = dict(
        operating_pressure=operating_pressure_cls,
        equilibrium_operating_pressure=equilibrium_operating_pressure_cls,
    )

