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


class custom(NamedObject[phase_child], CreatableNamedObjectMixinOld[phase_child]):
    """
    'custom' child.
    """

    fluent_name = "custom"

    child_object_type: phase_child = phase_child
    """
    child_object_type of custom.
    """
    return_type = "<object object at 0x7f115b6a91d0>"
