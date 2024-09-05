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

from .current_exchange_density import current_exchange_density as current_exchange_density_cls
from .cathodic_transfer_coefficient import cathodic_transfer_coefficient as cathodic_transfer_coefficient_cls
from .equilibium_potential_1 import equilibium_potential as equilibium_potential_cls
from .molecular_weight_1 import molecular_weight as molecular_weight_cls
from .density_1 import density as density_cls
from .spliting_coefficient import spliting_coefficient as spliting_coefficient_cls

class li_plating(Group):
    """
    Set up Li-plating reaction parameters.
    """

    fluent_name = "li-plating"

    child_names = \
        ['current_exchange_density', 'cathodic_transfer_coefficient',
         'equilibium_potential', 'molecular_weight', 'density',
         'spliting_coefficient']

    _child_classes = dict(
        current_exchange_density=current_exchange_density_cls,
        cathodic_transfer_coefficient=cathodic_transfer_coefficient_cls,
        equilibium_potential=equilibium_potential_cls,
        molecular_weight=molecular_weight_cls,
        density=density_cls,
        spliting_coefficient=spliting_coefficient_cls,
    )

