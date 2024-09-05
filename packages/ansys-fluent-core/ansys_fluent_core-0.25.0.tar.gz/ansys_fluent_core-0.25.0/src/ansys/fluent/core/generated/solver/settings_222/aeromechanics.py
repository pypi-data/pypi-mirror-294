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

from .aeromechanics_child import aeromechanics_child


class aeromechanics(NamedObject[aeromechanics_child], CreatableNamedObjectMixinOld[aeromechanics_child]):
    """
    'aeromechanics' child.
    """

    fluent_name = "aeromechanics"

    child_object_type: aeromechanics_child = aeromechanics_child
    """
    child_object_type of aeromechanics.
    """
    return_type = "<object object at 0x7f57023d26d0>"
