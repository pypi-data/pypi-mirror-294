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

from .list import list as list_cls
from .list_properties import list_properties as list_properties_cls
from .duplicate import duplicate as duplicate_cls
from .particle_mixture_child import particle_mixture_child


class particle_mixture(NamedObject[particle_mixture_child], CreatableNamedObjectMixinOld[particle_mixture_child]):
    """
    'particle_mixture' child.
    """

    fluent_name = "particle-mixture"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: particle_mixture_child = particle_mixture_child
    """
    child_object_type of particle_mixture.
    """
    return_type = "<object object at 0x7f641e62c0e0>"
