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

from .ec_concentration import ec_concentration as ec_concentration_cls
from .ec_diffusivity import ec_diffusivity as ec_diffusivity_cls
from .ionic_conductivity import ionic_conductivity as ionic_conductivity_cls
from .rate_constant import rate_constant as rate_constant_cls
from .cathodic_transfer_coefficient import cathodic_transfer_coefficient as cathodic_transfer_coefficient_cls
from .equilibium_potential import equilibium_potential as equilibium_potential_cls
from .molecular_weight import molecular_weight as molecular_weight_cls
from .density import density as density_cls

class sei_growth(Group):
    """
    Set up SEI layer growth parameters.
    """

    fluent_name = "sei-growth"

    child_names = \
        ['ec_concentration', 'ec_diffusivity', 'ionic_conductivity',
         'rate_constant', 'cathodic_transfer_coefficient',
         'equilibium_potential', 'molecular_weight', 'density']

    _child_classes = dict(
        ec_concentration=ec_concentration_cls,
        ec_diffusivity=ec_diffusivity_cls,
        ionic_conductivity=ionic_conductivity_cls,
        rate_constant=rate_constant_cls,
        cathodic_transfer_coefficient=cathodic_transfer_coefficient_cls,
        equilibium_potential=equilibium_potential_cls,
        molecular_weight=molecular_weight_cls,
        density=density_cls,
    )

