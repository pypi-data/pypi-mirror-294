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

from .species_child import species_child


class species(NamedObject[species_child], _NonCreatableNamedObjectMixin[species_child]):
    """
    'species' child.
    """

    fluent_name = "species"

    child_object_type: species_child = species_child
    """
    child_object_type of species.
    """
    return_type = "<object object at 0x7f115b6aa0c0>"
