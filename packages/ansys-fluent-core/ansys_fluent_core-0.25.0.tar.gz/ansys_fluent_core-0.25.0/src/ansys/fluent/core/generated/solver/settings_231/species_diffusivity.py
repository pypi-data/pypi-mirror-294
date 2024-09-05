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

from .species_diffusivity_child import species_diffusivity_child


class species_diffusivity(NamedObject[species_diffusivity_child], _NonCreatableNamedObjectMixin[species_diffusivity_child]):
    """
    'species_diffusivity' child.
    """

    fluent_name = "species-diffusivity"

    child_object_type: species_diffusivity_child = species_diffusivity_child
    """
    child_object_type of species_diffusivity.
    """
    return_type = "<object object at 0x7f115c1a5700>"
