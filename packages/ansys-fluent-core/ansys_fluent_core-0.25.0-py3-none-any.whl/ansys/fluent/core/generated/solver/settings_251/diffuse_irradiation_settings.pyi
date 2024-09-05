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

from typing import Union, List, Tuple

from .diffuse_irradiation_band import diffuse_irradiation_band as diffuse_irradiation_band_cls
from .diffuse_fraction_band import diffuse_fraction_band as diffuse_fraction_band_cls

class diffuse_irradiation_settings(Group):
    fluent_name = ...
    child_names = ...
    diffuse_irradiation_band: diffuse_irradiation_band_cls = ...
    diffuse_fraction_band: diffuse_fraction_band_cls = ...
