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

from .fluid_child import fluid_child


class mixture_species(NamedObject[fluid_child], CreatableNamedObjectMixinOld[fluid_child]):
    """
    'mixture_species' child.
    """

    fluent_name = "mixture-species"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of mixture_species.
    """
    return_type = "<object object at 0x7f571a5e0130>"
