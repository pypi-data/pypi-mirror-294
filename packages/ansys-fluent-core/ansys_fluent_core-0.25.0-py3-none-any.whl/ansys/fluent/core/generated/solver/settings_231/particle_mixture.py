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

from .particle_mixture_child import particle_mixture_child


class particle_mixture(NamedObject[particle_mixture_child], CreatableNamedObjectMixinOld[particle_mixture_child]):
    """
    'particle_mixture' child.
    """

    fluent_name = "particle-mixture"

    child_object_type: particle_mixture_child = particle_mixture_child
    """
    child_object_type of particle_mixture.
    """
    return_type = "<object object at 0x7f115c69b680>"
