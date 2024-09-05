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


class combusting_particle(NamedObject[fluid_child], CreatableNamedObjectMixinOld[fluid_child]):
    """
    'combusting_particle' child.
    """

    fluent_name = "combusting-particle"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of combusting_particle.
    """
    return_type = "<object object at 0x7f5719082f00>"
