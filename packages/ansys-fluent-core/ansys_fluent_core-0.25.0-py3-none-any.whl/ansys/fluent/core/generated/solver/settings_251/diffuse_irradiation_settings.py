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

from .diffuse_irradiation_band import diffuse_irradiation_band as diffuse_irradiation_band_cls
from .diffuse_fraction_band import diffuse_fraction_band as diffuse_fraction_band_cls

class diffuse_irradiation_settings(Group):
    """
    Diffuse irradiation settings.
    """

    fluent_name = "diffuse-irradiation-settings"

    child_names = \
        ['diffuse_irradiation_band', 'diffuse_fraction_band']

    _child_classes = dict(
        diffuse_irradiation_band=diffuse_irradiation_band_cls,
        diffuse_fraction_band=diffuse_fraction_band_cls,
    )

    _child_aliases = dict(
        band_diffuse_frac="diffuse_fraction_band",
        band_q_irrad_diffuse="diffuse_irradiation_band",
    )

