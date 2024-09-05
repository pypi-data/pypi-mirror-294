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
from .inert_particle_child import inert_particle_child


class inert_particle(NamedObject[inert_particle_child], CreatableNamedObjectMixinOld[inert_particle_child]):
    """
    'inert_particle' child.
    """

    fluent_name = "inert-particle"

    command_names = \
        ['list', 'list_properties', 'duplicate']

    _child_classes = dict(
        list=list_cls,
        list_properties=list_properties_cls,
        duplicate=duplicate_cls,
    )

    child_object_type: inert_particle_child = inert_particle_child
    """
    child_object_type of inert_particle.
    """
    return_type = "<object object at 0x7f641e5a4fe0>"
