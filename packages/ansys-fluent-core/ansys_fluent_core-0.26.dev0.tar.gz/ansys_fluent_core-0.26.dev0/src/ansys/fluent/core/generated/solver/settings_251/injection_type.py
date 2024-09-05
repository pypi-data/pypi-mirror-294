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

from .option_15 import option as option_cls
from .cone_type import cone_type as cone_type_cls
from .mass_flux_distribution import mass_flux_distribution as mass_flux_distribution_cls
from .inject_as_film import inject_as_film as inject_as_film_cls
from .filename_2_1 import filename_2 as filename_2_cls

class injection_type(Group):
    """
    'injection_type' child.
    """

    fluent_name = "injection-type"

    child_names = \
        ['option', 'cone_type', 'mass_flux_distribution', 'inject_as_film',
         'filename']

    _child_classes = dict(
        option=option_cls,
        cone_type=cone_type_cls,
        mass_flux_distribution=mass_flux_distribution_cls,
        inject_as_film=inject_as_film_cls,
        filename=filename_2_cls,
    )

    _child_aliases = dict(
        uniform_massflow_distribution_enabled="mass_flux_distribution",
    )

