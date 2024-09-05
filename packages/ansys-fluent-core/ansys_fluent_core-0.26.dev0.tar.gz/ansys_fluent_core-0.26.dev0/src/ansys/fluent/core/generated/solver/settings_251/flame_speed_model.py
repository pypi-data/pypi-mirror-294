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

from .flame_speed import flame_speed as flame_speed_cls
from .turbulent_length_scale_constant import turbulent_length_scale_constant as turbulent_length_scale_constant_cls
from .turbulent_flame_speed_constant import turbulent_flame_speed_constant as turbulent_flame_speed_constant_cls
from .stretch_factor_coeff import stretch_factor_coeff as stretch_factor_coeff_cls
from .wall_damping_coeff import wall_damping_coeff as wall_damping_coeff_cls
from .turbulent_schmidt_number import turbulent_schmidt_number as turbulent_schmidt_number_cls
from .turbulent_length_scale_constant_rans import turbulent_length_scale_constant_rans as turbulent_length_scale_constant_rans_cls
from .turbulent_flame_speed_constant_rans import turbulent_flame_speed_constant_rans as turbulent_flame_speed_constant_rans_cls
from .ewald_corrector import ewald_corrector as ewald_corrector_cls
from .blint_modifier import blint_modifier as blint_modifier_cls

class flame_speed_model(Group):
    """
    Turbulence Flame Speed Options.
    """

    fluent_name = "flame-speed-model"

    child_names = \
        ['flame_speed', 'turbulent_length_scale_constant',
         'turbulent_flame_speed_constant', 'stretch_factor_coeff',
         'wall_damping_coeff', 'turbulent_schmidt_number',
         'turbulent_length_scale_constant_rans',
         'turbulent_flame_speed_constant_rans', 'ewald_corrector',
         'blint_modifier']

    _child_classes = dict(
        flame_speed=flame_speed_cls,
        turbulent_length_scale_constant=turbulent_length_scale_constant_cls,
        turbulent_flame_speed_constant=turbulent_flame_speed_constant_cls,
        stretch_factor_coeff=stretch_factor_coeff_cls,
        wall_damping_coeff=wall_damping_coeff_cls,
        turbulent_schmidt_number=turbulent_schmidt_number_cls,
        turbulent_length_scale_constant_rans=turbulent_length_scale_constant_rans_cls,
        turbulent_flame_speed_constant_rans=turbulent_flame_speed_constant_rans_cls,
        ewald_corrector=ewald_corrector_cls,
        blint_modifier=blint_modifier_cls,
    )

