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

from .phase_child_10 import phase_child


class injection(NamedObject[phase_child], CreatableNamedObjectMixinOld[phase_child]):
    """
    'injection' child.
    """

    fluent_name = "injection"

    child_object_type: phase_child = phase_child
    """
    child_object_type of injection.
    """
    return_type = "<object object at 0x7f57023d2640>"
