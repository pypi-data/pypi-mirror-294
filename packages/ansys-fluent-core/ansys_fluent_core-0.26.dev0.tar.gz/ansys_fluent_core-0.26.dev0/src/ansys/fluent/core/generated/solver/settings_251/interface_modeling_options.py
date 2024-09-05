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

from .interface_type import interface_type as interface_type_cls
from .anti_diffusion import anti_diffusion as anti_diffusion_cls
from .anti_diffusion_factor import anti_diffusion_factor as anti_diffusion_factor_cls
from .zonal_discretization import zonal_discretization as zonal_discretization_cls
from .phase_localized_discretization import phase_localized_discretization as phase_localized_discretization_cls

class interface_modeling_options(Group):
    """
    Interface modeling.
    """

    fluent_name = "interface-modeling-options"

    child_names = \
        ['interface_type', 'anti_diffusion', 'anti_diffusion_factor',
         'zonal_discretization', 'phase_localized_discretization']

    _child_classes = dict(
        interface_type=interface_type_cls,
        anti_diffusion=anti_diffusion_cls,
        anti_diffusion_factor=anti_diffusion_factor_cls,
        zonal_discretization=zonal_discretization_cls,
        phase_localized_discretization=phase_localized_discretization_cls,
    )

