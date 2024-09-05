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

from .direct_irradiation import direct_irradiation as direct_irradiation_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .reference_direction_1 import reference_direction as reference_direction_cls

class direct_irradiation_settings(Group):
    """
    Direct irradiation settings.
    """

    fluent_name = "direct-irradiation-settings"

    child_names = \
        ['direct_irradiation', 'parallel_collimated_beam',
         'reference_direction']

    _child_classes = dict(
        direct_irradiation=direct_irradiation_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        reference_direction=reference_direction_cls,
    )

    _child_aliases = dict(
        band_q_irrad="direct_irradiation",
        component_of_radiation_direction="reference_direction",
    )

