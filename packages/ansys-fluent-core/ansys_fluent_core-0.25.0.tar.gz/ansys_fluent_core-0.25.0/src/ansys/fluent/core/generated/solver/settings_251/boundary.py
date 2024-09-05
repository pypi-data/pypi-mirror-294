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

from .fuel_temperature import fuel_temperature as fuel_temperature_cls
from .oxidizer_temperature import oxidizer_temperature as oxidizer_temperature_cls
from .species_boundary import species_boundary as species_boundary_cls
from .specify_species_in import specify_species_in as specify_species_in_cls

class boundary(Group):
    """
    PDF Boundary Options.
    """

    fluent_name = "boundary"

    child_names = \
        ['fuel_temperature', 'oxidizer_temperature', 'species_boundary',
         'specify_species_in']

    _child_classes = dict(
        fuel_temperature=fuel_temperature_cls,
        oxidizer_temperature=oxidizer_temperature_cls,
        species_boundary=species_boundary_cls,
        specify_species_in=specify_species_in_cls,
    )

