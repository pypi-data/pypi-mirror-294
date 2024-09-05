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

from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_ice_icing_mode import fensapice_ice_icing_mode as fensapice_ice_icing_mode_cls
from .fensapice_ice_hflux_mode import fensapice_ice_hflux_mode as fensapice_ice_hflux_mode_cls
from .fensapice_ice_hflux_value import fensapice_ice_hflux_value as fensapice_ice_hflux_value_cls
from .fensapice_ice_hflux_file import fensapice_ice_hflux_file as fensapice_ice_hflux_file_cls
from .fensapice_ice_wall_thickness import fensapice_ice_wall_thickness as fensapice_ice_wall_thickness_cls
from .fensapice_ice_wall_internal_temperature import fensapice_ice_wall_internal_temperature as fensapice_ice_wall_internal_temperature_cls
from .fensapice_ice_wall_conductivity import fensapice_ice_wall_conductivity as fensapice_ice_wall_conductivity_cls
from .fensapice_drop_vwet import fensapice_drop_vwet as fensapice_drop_vwet_cls
from .fensapice_drop_reinj import fensapice_drop_reinj as fensapice_drop_reinj_cls
from .fensapice_dpm_wall_condition import fensapice_dpm_wall_condition as fensapice_dpm_wall_condition_cls
from .fensapice_dpm_udf_wall_cond import fensapice_dpm_udf_wall_cond as fensapice_dpm_udf_wall_cond_cls
from .fensapice_dpm_bc_norm_coeff import fensapice_dpm_bc_norm_coeff as fensapice_dpm_bc_norm_coeff_cls
from .fensapice_dpm_bc_tang_coeff import fensapice_dpm_bc_tang_coeff as fensapice_dpm_bc_tang_coeff_cls

class icing(Group):
    """
    Allows to change icing model variables or settings.
    """

    fluent_name = "icing"

    child_names = \
        ['fensapice_flow_bc_subtype', 'fensapice_ice_icing_mode',
         'fensapice_ice_hflux_mode', 'fensapice_ice_hflux_value',
         'fensapice_ice_hflux_file', 'fensapice_ice_wall_thickness',
         'fensapice_ice_wall_internal_temperature',
         'fensapice_ice_wall_conductivity', 'fensapice_drop_vwet',
         'fensapice_drop_reinj', 'fensapice_dpm_wall_condition',
         'fensapice_dpm_udf_wall_cond', 'fensapice_dpm_bc_norm_coeff',
         'fensapice_dpm_bc_tang_coeff']

    _child_classes = dict(
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_ice_icing_mode=fensapice_ice_icing_mode_cls,
        fensapice_ice_hflux_mode=fensapice_ice_hflux_mode_cls,
        fensapice_ice_hflux_value=fensapice_ice_hflux_value_cls,
        fensapice_ice_hflux_file=fensapice_ice_hflux_file_cls,
        fensapice_ice_wall_thickness=fensapice_ice_wall_thickness_cls,
        fensapice_ice_wall_internal_temperature=fensapice_ice_wall_internal_temperature_cls,
        fensapice_ice_wall_conductivity=fensapice_ice_wall_conductivity_cls,
        fensapice_drop_vwet=fensapice_drop_vwet_cls,
        fensapice_drop_reinj=fensapice_drop_reinj_cls,
        fensapice_dpm_wall_condition=fensapice_dpm_wall_condition_cls,
        fensapice_dpm_udf_wall_cond=fensapice_dpm_udf_wall_cond_cls,
        fensapice_dpm_bc_norm_coeff=fensapice_dpm_bc_norm_coeff_cls,
        fensapice_dpm_bc_tang_coeff=fensapice_dpm_bc_tang_coeff_cls,
    )

