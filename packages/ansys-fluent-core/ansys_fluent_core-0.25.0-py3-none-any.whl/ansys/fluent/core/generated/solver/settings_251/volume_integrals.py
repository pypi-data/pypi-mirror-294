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

from .mass_average import mass_average as mass_average_cls
from .mass_integral import mass_integral as mass_integral_cls
from .mass import mass as mass_cls
from .sum_1 import sum as sum_cls
from .twopisum import twopisum as twopisum_cls
from .minimum_5 import minimum as minimum_cls
from .maximum_5 import maximum as maximum_cls
from .volume_2 import volume as volume_cls
from .volume_average import volume_average as volume_average_cls
from .volume_integral import volume_integral as volume_integral_cls
from .get_mass_average import get_mass_average as get_mass_average_cls
from .get_mass_integral import get_mass_integral as get_mass_integral_cls
from .get_mass import get_mass as get_mass_cls
from .get_sum_1 import get_sum as get_sum_cls
from .get_twopisum import get_twopisum as get_twopisum_cls
from .get_minimum import get_minimum as get_minimum_cls
from .get_maximum import get_maximum as get_maximum_cls
from .get_volume import get_volume as get_volume_cls
from .get_volume_average import get_volume_average as get_volume_average_cls
from .compute_volume_integral import compute_volume_integral as compute_volume_integral_cls

class volume_integrals(Group):
    """
    'volume_integrals' child.
    """

    fluent_name = "volume-integrals"

    command_names = \
        ['mass_average', 'mass_integral', 'mass', 'sum', 'twopisum',
         'minimum', 'maximum', 'volume', 'volume_average', 'volume_integral']

    query_names = \
        ['get_mass_average', 'get_mass_integral', 'get_mass', 'get_sum',
         'get_twopisum', 'get_minimum', 'get_maximum', 'get_volume',
         'get_volume_average', 'compute_volume_integral']

    _child_classes = dict(
        mass_average=mass_average_cls,
        mass_integral=mass_integral_cls,
        mass=mass_cls,
        sum=sum_cls,
        twopisum=twopisum_cls,
        minimum=minimum_cls,
        maximum=maximum_cls,
        volume=volume_cls,
        volume_average=volume_average_cls,
        volume_integral=volume_integral_cls,
        get_mass_average=get_mass_average_cls,
        get_mass_integral=get_mass_integral_cls,
        get_mass=get_mass_cls,
        get_sum=get_sum_cls,
        get_twopisum=get_twopisum_cls,
        get_minimum=get_minimum_cls,
        get_maximum=get_maximum_cls,
        get_volume=get_volume_cls,
        get_volume_average=get_volume_average_cls,
        compute_volume_integral=compute_volume_integral_cls,
    )

