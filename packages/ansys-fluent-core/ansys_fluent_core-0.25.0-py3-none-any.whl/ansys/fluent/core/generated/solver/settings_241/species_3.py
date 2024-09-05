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

from .volumetric_species import volumetric_species as volumetric_species_cls
from .last_species import last_species as last_species_cls

class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['volumetric_species', 'last_species']

    _child_classes = dict(
        volumetric_species=volumetric_species_cls,
        last_species=last_species_cls,
    )

    return_type = "<object object at 0x7f5d0866a0c0>"
